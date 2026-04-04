# OhStem-compatible RTOS-style blink example for YoloUno
#
# Prefers OhStem `pins` / `led_strip`; falls back to machine.Pin + neopixel.

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio  # type: ignore


def hex_to_rgb(hex_color: str):
    """Convert '#RRGGBB' to (r, g, b)."""
    s = hex_color.strip().lstrip("#")
    if len(s) != 6:
        raise ValueError("hex color must be in '#RRGGBB' format")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


async def asleep_ms(ms: int):
    if hasattr(asyncio, "sleep_ms"):
        await asyncio.sleep_ms(ms)
    else:
        await asyncio.sleep(ms / 1000)


def create_task(coro):
    return asyncio.create_task(coro)


# --- Hardware init ---
NEO_COLOR_RED = hex_to_rgb("#ff0000")
NEO_COLOR_OFF = (0, 0, 0)

USE_OHSTEM = False
try:
    from pins import *  # noqa: F401,F403
    from led_strip import *  # noqa: F401,F403

    led_D3 = Pins(D3_PIN)
    strips = Led_Strip(D3_PIN, 30)
    neopix = strips  # OhStem code view often uses neopix.show(...)
    USE_OHSTEM = True
except Exception:
    from machine import Pin
    import neopixel

    # Adjust GPIO numbers if this fallback path is used on your board.
    LED_D3_GPIO = 48
    NEO_PIN_GPIO = 45
    led_D3 = Pin(LED_D3_GPIO, Pin.OUT)
    neopix = neopixel.NeoPixel(Pin(NEO_PIN_GPIO), 1)


def set_led_d3(on: bool):
    if USE_OHSTEM:
        led_D3.write_digital(1 if on else 0)
    else:
        led_D3.value(1 if on else 0)


def neopix_show(color):
    if USE_OHSTEM:
        neopix.show(0, color)
    else:
        neopix[0] = color
        neopix.write()


# --- RTOS-style tasks (uasyncio) ---
async def task_on_message_1():
    neopix_show(NEO_COLOR_RED)


async def task_blinky_led_d3():
    while True:
        await asleep_ms(250)
        set_led_d3(True)
        await asleep_ms(250)
        set_led_d3(False)


async def task_blinky_neopix():
    while True:
        await asleep_ms(1000)
        neopix_show(NEO_COLOR_RED)
        await asleep_ms(500)
        neopix_show(NEO_COLOR_OFF)


async def main():
    print("App started")
    create_task(task_on_message_1())
    create_task(task_blinky_led_d3())
    create_task(task_blinky_neopix())
    while True:
        await asleep_ms(100)


try:
    asyncio.run(main())
except Exception:
    # Some MicroPython builds do not support asyncio.run.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

