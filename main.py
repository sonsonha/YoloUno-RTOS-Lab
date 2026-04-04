
# Loader for YoloUno: runs the RTOS-style blink demo.
#
# On MicroPython, the firmware runs `main.py` after `boot.py`.
# Import `main_rtos` so the async blink tasks start at boot.

# LAB 3: Task communication via asyncio.Event (semaphore-style signal)
# Yolo UNO / ESP32-S3 MicroPython — entry file: firmware chạy `main.py` sau reset.
#
# - button_task: BOOT GPIO0, pull-up, pressed = 0 → button_event.set()
# - worker_task: await Event → clear → toggle LED (GPIO48, giống Lab2)

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from machine import Pin


async def asleep_ms(ms):
    if hasattr(asyncio, "sleep_ms"):
        await asyncio.sleep_ms(ms)
    else:
        await asyncio.sleep(ms / 1000)


def create_task(coro):
    return asyncio.create_task(coro)


BOOT_BUTTON_GPIO = 0
LED_PIN_GPIO = 48

button = Pin(BOOT_BUTTON_GPIO, Pin.IN, Pin.PULL_UP)
led = Pin(LED_PIN_GPIO, Pin.OUT)
led.value(0)

button_event = asyncio.Event()


async def button_task():
    last = button.value()
    while True:
        v = button.value()
        if last == 1 and v == 0:
            button_event.set()
            print("button_task: event set")
            await asleep_ms(180)
        last = v
        await asleep_ms(20)


async def worker_task():
    led_on = False
    while True:
        await button_event.wait()
        button_event.clear()
        led_on = not led_on
        led.value(1 if led_on else 0)
        print("worker_task: LED", "ON" if led_on else "OFF")


async def main():
    print("LAB3 started (Event ~ semaphore)")
    create_task(button_task())
    create_task(worker_task())
    while True:
        await asleep_ms(500)


try:
    asyncio.run(main())
except Exception:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

