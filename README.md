# Yolo UNO MicroPython Labs (VSCode)

This repository is used to teach MicroPython on Yolo UNO (ESP32-S3).
For all labs (`lab1`, `lab2`, `lab3`), students use the same upload flow:

- macOS: `Cmd + Shift + B`
- Windows: `Ctrl + Shift + B`

## 1) One-time setup

1. Install [VSCode](https://code.visualstudio.com/).
2. Install Python 3.
3. Install VSCode extensions:
   - `ms-python.python`
   - `ms-python.vscode-pylance`
   - `pycom.Pymakr` (optional, for serial tools)
4. Install `mpremote`:

```bash
python -m pip install mpremote
```

## 2) Open the correct folder in VSCode

Open `pymakr_project/` as the working folder.

This folder includes:
- `main.py`
- `lcd_i2c.py`
- `.vscode/tasks.json` (preconfigured upload tasks)

## 3) Upload with one shortcut (all labs)

1. Connect Yolo UNO by USB.
2. Close any open serial monitor/REPL.
3. Press build shortcut:
   - macOS: `Cmd + Shift + B`
   - Windows: `Ctrl + Shift + B`
4. Select `Upload via mpremote`.
5. When prompted, enter serial port:
   - macOS example: `/dev/cu.usbmodem1234561`
   - Windows example: `COM3`

The task uploads `main.py` and `lcd_i2c.py`, then resets the board.

## 3.1) Lab 2 quick guide (Vietnamese)

Lab 2 goal: read sensor values and display them on LCD.

### Setup once

1. Cắm board Yolo UNO qua USB.
2. Mở thư mục `pymakr_project` trong VSCode.
3. Đảm bảo đã cài `mpremote`:

```bash
python -m pip install mpremote
```

### Nạp code bằng một phím tắt

1. Đóng Serial Monitor/REPL nếu đang mở.
2. Bấm:
   - macOS: `Cmd + Shift + B`
   - Windows: `Ctrl + Shift + B`
3. Chọn `Upload via mpremote`.
4. Nhập cổng serial:
   - macOS: `/dev/cu.usbmodem1234561` (hoặc cổng đang có trên máy)
   - Windows: `COM3`/`COM4`/...
5. Chờ task chạy xong, board tự reset và chạy `main.py`.

### Kiểm tra sau khi nạp

- Mở task `Open REPL` để xem log.
- Nếu đúng Lab 2, bạn sẽ thấy log đọc nhiệt độ/độ ẩm và LCD cập nhật theo chu kỳ.

## 4) Other useful tasks

- `Upload main.py only` (faster when only `main.py` changed)
- `Open REPL`
- `List files on board`

## 5) Common issues

### `ValueError: odd-length string` (Pymakr upload)
Use build task upload (`Cmd/Ctrl + Shift + B`) instead of Pymakr folder upload.

### `failed to access ... it may be in use by another program`
- Close serial tools (Pymakr terminal, Arduino Serial Monitor, Thonny, other `mpremote`).
- Unplug/replug USB cable.
- Upload again.

### Wrong port
- macOS ports are usually `/dev/cu.usbmodem...`
- Windows ports are usually `COM3`, `COM4`, etc.

## 6) Lab note

The upload workflow is shared for all labs.
Only lab code changes, upload steps stay the same.

