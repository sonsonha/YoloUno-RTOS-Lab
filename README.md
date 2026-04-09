# YoloUno MicroPython Labs (main branch handbook)

This document is the main-branch guide for the whole project: setup, uploading code with the keyboard shortcut (`Cmd + Shift + B` / `Ctrl + Shift + B`), troubleshooting failed uploads, an overview of lab branches, and notes for teaching.

## 1) Repository overview

- Board: **YoloUno** (ESP32-S3 running MicroPython firmware).
- Goal: write Python directly in VS Code without block-based drag-and-drop.
- Main folders:
  - `pymakr_project/`: sources that get flashed to the board.
  - `.vscode/tasks.json`: build tasks for quick upload via shortcut.
  - `README.md`: this handbook.

## 2) Lab branches

- `lab1`: LED + NeoPixel, basic async/cooperative multitasking.
- `lab2`: GPIO + I2C (DHT20/LCD), sensor readout and display.
- `lab3`: semaphore / mode switching, built on lab2.
- `main`: combined handbook + shared documentation.

Before you flash, always confirm you are on the correct branch:

```bash
git branch --show-current
```

## 3) Prerequisites

1. A **USB data cable** (not charge-only).
2. Board flashed with a **compatible MicroPython** firmware.
3. **Node.js** (LTS recommended) — **required** so you can upload/sync the project from VS Code using the **Pymakr** extension (the extension relies on the Node.js runtime). Install from [https://nodejs.org/](https://nodejs.org/) and verify with `node -v` and `npm -v`.
4. **VS Code** installed.
5. **Python 3** installed.
6. VS Code extensions:
   - `ms-python.python`
   - `ms-python.vscode-pylance`
   - `pycom.Pymakr` (recommended for REPL/serial and project upload)
7. **mpremote** (for stable uploads via build tasks):

```bash
python -m pip install mpremote
```

> **Note:** If you only use **mpremote** from the terminal or the **Upload via mpremote** build task, Python + mpremote are enough for that path. **Uploading/syncing the folder through the Pymakr UI still requires Node.js** (and the Pymakr extension).

## 4) Setup so `Cmd/Ctrl + Shift + B` can upload

The project already defines build tasks. Steps:

1. Open the project folder in VS Code (`Yolouno-micropython` or `pymakr_project`).
2. Connect the YoloUno board over USB.
3. Close any Serial Monitor / REPL windows that hold the port.
4. Press:
   - **macOS:** `Cmd + Shift + B`
   - **Windows:** `Ctrl + Shift + B`
5. Pick the upload task (`Upload via mpremote`, `Upload Lab1 via mpremote`, etc., depending on branch).
6. Enter the serial port when prompted:
   - macOS: e.g. `/dev/cu.usbmodem1234561`
   - Windows: e.g. `COM3`, `COM4`
7. Wait until the task finishes; the board resets and runs `main.py`.

## 5) How to find the serial port

- **macOS:** usually `/dev/cu.usbmodem...` or `/dev/cu.usbserial...`
- **Windows:** Device Manager → `Ports (COM & LPT)` → note `COMx`

If unsure, unplug and replug the board and see which port appears or disappears.

## 6) Troubleshooting when upload fails

### A. `ValueError: odd-length string` (Pymakr)

- Common cause: folder upload through Pymakr breaks during hex/serialization transfer.
- Fix: use the build task (`Cmd/Ctrl + Shift + B`) with **mpremote**, or ensure **Node.js** is installed and retry Pymakr sync.

### B. `failed to access ... it may be in use by another program`

- Another app is holding the serial port.
- Close Pymakr terminal, Arduino Serial Monitor, Thonny, old mpremote sessions.
- Unplug/replug USB and upload again.

### C. `Cmd/Ctrl + Shift + B` shows no upload task

- Wrong folder/workspace opened.
- Use `File → Open Folder` and open `Yolouno-micropython` or `pymakr_project`.
- Reload the VS Code window (`Developer: Reload Window`).

### D. VS Code reports `Import "machine" / "uasyncio" could not be resolved`

- This is a **Pylance warning on the PC**, not a firmware error on the board.
- If the code runs on the board after upload, you can ignore it.

### E. LCD shows wrong content (e.g. old lab code)

- Check that the upload task copies all needed files (`main.py`, `main_rtos.py`, `lcd_i2c.py` as required).
- Run a full upload task instead of `main.py` only.

## 7) Suggested flow for students

1. `git checkout <lab-branch>`
2. Open the correct project folder.
3. Plug in the board.
4. Press `Cmd/Ctrl + Shift + B`.
5. Choose the upload task.
6. Enter the correct port.
7. Verify behavior with **Open REPL** (Pymakr).

## 8) Important notes

- Only **one** program may use the serial port at a time.
- Always confirm the **git branch** before flashing.
- When the task asks for a port, use the right format for your OS (`/dev/cu...` vs `COMx`).
- Prefer **mpremote** build tasks for more reliable uploads than Pymakr folder sync alone.
- Before class, do a quick test on both macOS and Windows if possible.
