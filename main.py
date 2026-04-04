# Loader for YoloUno: runs the RTOS-style blink demo.
#
# On MicroPython, the firmware runs `main.py` after `boot.py`.
# Import `main_rtos` so the async blink tasks start at boot.
import main_rtos  # noqa: F401
