# Loader file for Yolo UNO (runs RTOS-style blink)
#
# Về phía MicroPython, firmware luôn chạy `main.py` sau `boot.py`.
# Nên ta chỉ cần import `main_rtos.py` để thực thi code RTOS blink.
import main_rtos
