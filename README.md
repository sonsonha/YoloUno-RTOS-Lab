# Yolo UNO MicroPython Labs in VSCode

This repository is used for teaching MicroPython on **Yolo UNO (ESP32-S3)**.
Students write code in VSCode and upload to the board using a shared workflow for all labs.

## Project Layout

```text
Yolouno-micropython/
├── pymakr_project/
│   ├── main.py
│   ├── main_rtos.py
│   ├── lcd_i2c.py
│   ├── pymakr.json
│   └── .pymakr-ignore
├── .vscode/
│   ├── settings.json
│   └── tasks.json
└── README.md
```

- `pymakr_project/` contains files uploaded to the board.
- `.vscode/tasks.json` contains the upload tasks used by students.

## One-Time Setup

### 1) Install tools

- Install [VSCode](https://code.visualstudio.com/)
- Install Python 3
- Install VSCode extensions:
  - `ms-python.python`
  - `ms-python.vscode-pylance`
  - `pycom.Pymakr` (optional for REPL/port management)

### 2) Install `mpremote`

Use one of the following:

```bash
pip3 install mpremote
```

or

```bash
python -m pip install mpremote
```

### 3) Open this folder in VSCode

Open `Yolouno-micropython` as the workspace root.
The upload tasks are already preconfigured.

## Shared Upload Workflow (Lab 1, Lab 2, Lab 3)

Use this same method for every lab.

1. Connect Yolo UNO via USB.
2. Close serial monitor/REPL windows if they are open.
3. Press:
   - **macOS:** `Cmd + Shift + B`
   - **Windows:** `Ctrl + Shift + B`
4. Select task:
   - `Upload via mpremote` (recommended)
   - or `Upload main.py only`
5. Wait until upload completes and board resets.

This workflow is preferred over folder upload in Pymakr because it is more stable in class use.

## Run and Debug

- To open REPL:
  - run task `Open REPL`, or
  - use terminal command:
    - macOS:
      ```bash
      mpremote connect /dev/cu.usbmodem1234561 repl
      ```
    - Windows:
      ```bash
      mpremote connect COM3 repl
      ```
- Press `Ctrl + C` in REPL to stop the current script.

## Port Names: macOS vs Windows

- **macOS:** usually `/dev/cu.usbmodem...`
- **Windows:** usually `COM3`, `COM4`, `COM5`, ...

If needed, update port in `.vscode/tasks.json` and `pymakr_project/pymakr.json`.

## Common Issues and Fixes

### 1) `ValueError: odd-length string` (Pymakr upload)

- Cause: Pymakr folder upload serialization issue.
- Fix: use Build Task upload (`Cmd/Ctrl + Shift + B`) with `mpremote`.

### 2) `failed to access ... it may be in use by another program`

- Close any serial tool (Pymakr terminal, Arduino Serial Monitor, Thonny, another `mpremote` session).
- Unplug/replug USB cable.
- Try upload again.

### 3) Board runs old code

- Ensure you uploaded the correct file (`main.py`).
- Use `Upload via mpremote` to upload both `main.py` and `lcd_i2c.py`.

## Labs

- `lab1`: basic LED and NeoPixel
- `lab2`: button, relay, DHT20, LCD over I2C
- `lab3`: mode switching with `uasyncio`/semaphore

The upload steps are the same for all labs.
