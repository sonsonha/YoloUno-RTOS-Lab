# LAB 3: Button cycles modes via asyncio.Semaphore (each press = release 1 token).
# Yolo UNO / ESP32-S3 - I2C/LCD/DHT20 same as Lab2 (see main_rtos.py). Lab2 branch not modified.
#
# Mode 1: LCD temp + humidity; NeoPixel blinks blue.
# Mode 2: LCD env status (Normal / Warning); green blink OK, red blink warn.
# Mode 3: LCD "Hello!"; NeoPixel cycles green -> blue -> red.
#
# NeoPixel default GPIO45 (README). Some boards use WS2812 on GPIO48 instead of D13-only LED.

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import time
from machine import I2C, Pin

try:
    from lcd_i2c import I2cLcd
except ImportError:
    I2cLcd = None


class _SemShim:
    """Counting semaphore if asyncio.Semaphore is missing on older MicroPython."""

    def __init__(self, value=0):
        self._tokens = value
        self._evt = asyncio.Event()
        if value > 0:
            self._evt.set()

    def release(self):
        self._tokens += 1
        self._evt.set()

    async def acquire(self):
        while True:
            if self._tokens > 0:
                self._tokens -= 1
                if self._tokens == 0:
                    self._evt.clear()
                return
            await self._evt.wait()


_SemType = asyncio.Semaphore if hasattr(asyncio, "Semaphore") else _SemShim


async def asleep_ms(ms):
    if hasattr(asyncio, "sleep_ms"):
        await asyncio.sleep_ms(ms)
    else:
        await asyncio.sleep(ms / 1000)


def create_task(coro):
    return asyncio.create_task(coro)


# --- Pins (match Lab2: Grove I2C + button) ---
# Use on-board BOOT button (ESP32-S3 GPIO0).
BUTTON_PIN_GPIO = 0
I2C_SDA_GPIO = 11
I2C_SCL_GPIO = 12
# Try 45 first (README); some Yolo UNO boards wire WS2812 to GPIO48.
NEOPIXEL_PIN = 45
NEOPIXEL_N = 1

MODE_MIN = 1
MODE_MAX = 3

# --- DHT20 (same pattern as Lab2) ---
class DHT20:
    ADDRESS = 0x38

    def __init__(self, i2c, address=ADDRESS):
        self.i2c = i2c
        self.address = address

    def _trigger_measure(self):
        self.i2c.writeto(self.address, b"\xAC\x33\x00")

    def _is_busy(self):
        status = self.i2c.readfrom(self.address, 1)[0]
        return (status & 0x80) != 0

    def read(self):
        self._trigger_measure()
        time.sleep_ms(90)
        for _ in range(10):
            if not self._is_busy():
                break
            time.sleep_ms(10)

        data = self.i2c.readfrom(self.address, 7)
        raw_h = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        raw_t = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = (raw_h * 100.0) / 1048576.0
        temperature = (raw_t * 200.0) / 1048576.0 - 50.0
        return temperature, humidity


button = Pin(BUTTON_PIN_GPIO, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(I2C_SCL_GPIO), sda=Pin(I2C_SDA_GPIO), freq=100000)
dht20 = None
lcd = None
np_led = None

_t = 0.0
_h = 0.0
_sensor_ok = False
mode = 1

mode_sem = _SemType(0)

RGB_OFF = (0, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_RED = (255, 0, 0)


def init_i2c_devices():
    global dht20, lcd
    devices = i2c.scan()
    print("I2C scan:", [hex(x) for x in devices])
    if DHT20.ADDRESS in devices:
        dht20 = DHT20(i2c)
    else:
        print("Warning: DHT20 not found on I2C.")
    lcd_candidates = (0x27, 0x3F, 0x21, 0x20, 0x22, 0x23, 0x24, 0x25, 0x26)
    lcd = None
    if I2cLcd is None:
        print("Warning: lcd_i2c module not found, LCD disabled.")
    else:
        for addr in lcd_candidates:
            if addr not in devices or addr == DHT20.ADDRESS:
                continue
            try:
                lcd = I2cLcd(i2c, addr=addr, cols=16, rows=2)
                print("LCD OK at", hex(addr))
                break
            except Exception as exc:
                print("LCD init failed at", hex(addr), ":", exc)
                lcd = None
        if lcd is None:
            print("Warning: LCD not found or init failed.")


def init_neopixel():
    global np_led
    try:
        import neopixel

        np_led = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_N)
        np_led[0] = RGB_OFF
        np_led.write()
        print("NeoPixel OK GPIO", NEOPIXEL_PIN)
    except Exception as exc:
        np_led = None
        print("NeoPixel disabled:", exc)


def np_set(color):
    if np_led is None:
        return
    np_led[0] = color
    np_led.write()


def env_eval():
    if not _sensor_ok:
        return False, "Warning!", "No sensor"
    warn = False
    if _t < 18.0 or _t > 32.0:
        warn = True
    if _h < 35.0 or _h > 75.0:
        warn = True
    if warn:
        return False, "Warning!", "Check T/H"
    return True, "Normal", "Env OK"


async def button_task():
    last = button.value()
    while True:
        v = button.value()
        if last == 1 and v == 0:
            mode_sem.release()
            print("button: sem release (mode advance)")
            await asleep_ms(180)
        last = v
        await asleep_ms(20)


async def mode_task():
    global mode
    while True:
        await mode_sem.acquire()
        if mode >= MODE_MAX:
            mode = MODE_MIN
        else:
            mode += 1
        print("mode ->", mode)


async def sensor_task():
    global _t, _h, _sensor_ok
    while True:
        if dht20:
            try:
                _t, _h = dht20.read()
                _sensor_ok = True
            except Exception as exc:
                _sensor_ok = False
                print("DHT20 read error:", exc)
        else:
            _sensor_ok = False
        await asleep_ms(2000)


async def ui_task():
    blink_on = True
    m3_idx = 0
    m3_colors = (RGB_GREEN, RGB_BLUE, RGB_RED)
    half_ms = 400

    while True:
        await asleep_ms(half_ms)
        blink_on = not blink_on

        if mode == 1:
            if lcd:
                if _sensor_ok:
                    lcd.write_line(0, "Temp:{:5.1f}C".format(_t))
                    lcd.write_line(1, "Humi:{:5.1f}%".format(_h))
                else:
                    lcd.write_line(0, "Temp/Humi")
                    lcd.write_line(1, "No DHT20")
            if blink_on:
                np_set(RGB_BLUE)
            else:
                np_set(RGB_OFF)

        elif mode == 2:
            ok, title, sub = env_eval()
            if lcd:
                lcd.write_line(0, title[:16])
                lcd.write_line(1, sub[:16])
            if ok:
                if blink_on:
                    np_set(RGB_GREEN)
                else:
                    np_set(RGB_OFF)
            else:
                if blink_on:
                    np_set(RGB_RED)
                else:
                    np_set(RGB_OFF)

        else:
            if lcd:
                lcd.write_line(0, "Hello!")
                lcd.write_line(1, "")
            if blink_on:
                np_set(m3_colors[m3_idx])
                m3_idx = (m3_idx + 1) % 3
            else:
                np_set(RGB_OFF)


async def main():
    print("LAB3 started (Semaphore + modes)")
    init_i2c_devices()
    init_neopixel()
    create_task(button_task())
    create_task(mode_task())
    create_task(sensor_task())
    create_task(ui_task())
    while True:
        await asleep_ms(1000)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
