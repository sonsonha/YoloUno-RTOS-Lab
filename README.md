# Yolo UNO - Lab 1 Upload Guide (Cmd/Ctrl + Shift + B)

Tai lieu nay dung cho branch `lab1`. Muc tieu la de sinh vien chi can bam mot phim tat de nap code.

## 1) Lab 1 includes

- `pymakr_project/main.py`: loader file.
- `pymakr_project/main_rtos.py`: blink LED + NeoPixel task.

Board se auto-run `main.py`, va `main.py` se import `main_rtos.py`.

## 2) One-time setup

1. Install VSCode.
2. Install Python 3.
3. Install VSCode extensions:
   - `ms-python.python`
   - `ms-python.vscode-pylance`
   - `pycom.Pymakr` (optional)
4. Install `mpremote`:

```bash
python -m pip install mpremote
```

## 3) Open project correctly

Open one of these in VSCode:
- Repo root `Yolouno-micropython`, or
- `pymakr_project/`

Both locations now have `.vscode/tasks.json`, so build shortcut works in both cases.

## 4) Upload with shortcut

### macOS
1. Plug in Yolo UNO.
2. Close any Serial Monitor/REPL.
3. Press `Cmd + Shift + B`.
4. Select `Upload Lab1 via mpremote`.
5. Enter serial port, for example: `/dev/cu.usbmodem1234561`.

### Windows
1. Plug in Yolo UNO.
2. Close any Serial Monitor/REPL.
3. Press `Ctrl + Shift + B`.
4. Select `Upload Lab1 via mpremote`.
5. Enter serial port, for example: `COM3` or `COM4`.

This task uploads both `main.py` and `main_rtos.py`, then resets the board.

## 5) Verify after upload

- Run task `Open REPL`.
- You should see `App started`.
- LED D3 and NeoPixel should blink according to Lab 1 logic.

## 6) Common issues

### `failed to access ... it may be in use by another program`
- Close Pymakr terminal, Arduino Serial Monitor, Thonny, and any old `mpremote` sessions.
- Unplug/replug USB.
- Run `Cmd/Ctrl + Shift + B` again.

### `ValueError: odd-length string` when uploading with Pymakr
- Do not use folder upload from Pymakr.
- Use build task upload (`Cmd/Ctrl + Shift + B`) only.

### Wrong serial port
- macOS usually: `/dev/cu.usbmodem...`
- Windows usually: `COMx`

## 7) Teacher note

For class use, ask students to follow exactly this flow:
- Open project
- Build shortcut
- Select `Upload Lab1 via mpremote`
- Enter correct serial port

