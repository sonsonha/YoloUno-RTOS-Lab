# YoloUno MicroPython labs (VS Code + Pymakr)

This repository contains **MicroPython** example code for the **YoloUno** board (ESP32-based), intended for hands-on labs. The same ideas underlie the [OhStem](https://ohstem.vn/) ecosystem: their drag-and-drop tools generate MicroPython behind the scenes. Here you work **directly in source code** in **Visual Studio Code** and upload to the board with the **Pymakr** extension (or compatible workflows), instead of using the OhStem block editor.

---

## Lab branches and how they build on each other

Labs are organized in **Git branches** (for example `lab1`, `lab2`, `lab3`). Each branch is a self-contained snapshot for that lab:

| Typical branch | Theme (curriculum) |
|----------------|-------------------|
| **Lab 1** | LEDs, “RTOS-style” concurrency with `uasyncio`, heartbeat / RGB indicator patterns |
| **Lab 2** | GPIO (button, LED, relay) and I2C peripherals (e.g. sensor + LCD) |
| **Lab 3** | Semaphores and task communication; Git workflow and pushing work |

**Dependency order:** Lab 2 extends Lab 1; Lab 3 extends Lab 2. Check out the branch your instructor assigns:

```bash
git fetch origin
git checkout lab1    # or lab2, lab3 — use the exact branch name from your course
```

Always confirm the active branch before you upload code (`git branch` or the VS Code status bar).

---

## What is in this project

### Folder layout

- **`pymakr_project/`** — Recommended folder to open in VS Code for Pymakr. It contains:
  - `pymakr.conf` — Serial port and Pymakr options (see below).
  - `main.py` — Entry point the firmware runs after `boot.py`.
  - `main_rtos.py` — Async “multi-task” demo (see [Understanding the code](#understanding-the-code)).
- **Repository root** may also contain `main.py` / `main_rtos.py` copies for browsing or tooling; **follow your instructor** on which copy is the source of truth for your lab branch.

### Firmware assumption

The board should already run a **MicroPython** firmware that matches your course (often the same image OhStem tooling uses). This repo **does not** replace flashing the interpreter; it provides **application** scripts (`main.py`, etc.) you sync to the device filesystem.

---

## Understanding the code

### `main.py` (loader)

MicroPython starts **`main.py`** automatically after `boot.py`. In this template, `main.py` only **imports** the real program so you can keep the async demo in a separate file:

```python
import main_rtos  # noqa: F401
```

Do not delete this import if your lab expects `main_rtos` to run at boot.

### `main_rtos.py` (async tasks)

This file illustrates **cooperative multitasking** with `uasyncio` (MicroPython’s asyncio). Conceptually it is similar to scheduling **tasks** on an RTOS: several loops run “in parallel” by **yielding** with `await sleep`.

Rough structure:

1. **Optional OhStem hardware API** — If the firmware provides `pins` and `led_strip`, the code uses `Pins`, `Led_Strip`, etc. (same style as OhStem “code view”).
2. **Fallback** — If those modules are missing, it uses `machine.Pin` and `neopixel` with GPIO numbers you can adjust for your board.
3. **Tasks**
   - One task sets the NeoPixel / strip to red once at start (`task_on_message_1`).
   - One task blinks the D3 LED with ~250 ms on/off (`task_blinky_led_d3`).
   - One task toggles the NeoPixel between red and off (`task_blinky_neopix`).
4. **Event loop** — `asyncio.run(main())` or a manual loop fallback for builds without `asyncio.run`.

**Pins (fallback mode, in code):** `LED_D3_GPIO = 48`, `NEO_PIN_GPIO = 45`. Change only if your hardware mapping differs and you are not using the OhStem `pins` module.

---

## Prerequisites (Windows and macOS)

1. **USB cable** that supports data (not charge-only).
2. **USB serial driver** if Windows does not recognize the board (common: CP210x, CH340, or the chip your YoloUno uses — follow the manufacturer’s guide).
3. **Visual Studio Code** — [https://code.visualstudio.com/](https://code.visualstudio.com/)
4. **Pymakr** extension — In VS Code, open Extensions, search for **Pymakr** (by Pycom / maintained ecosystem; install the current listing your instructor recommends).
5. **Git** — To clone the repo and switch lab branches: [https://git-scm.com/](https://git-scm.com/)

You do **not** need the OhStem block app to use this workflow; you only need MicroPython on the board and a working USB serial connection.

---

## Configure the serial port

### Find the port

**Windows**

- Device Manager → **Ports (COM & LPT)** — note `COM3`, `COM4`, etc.
- Or PowerShell: sometimes `Get-PnpDevice -Class Ports` helps identify the device.

**macOS**

- Common paths: `/dev/cu.usbmodem*`, `/dev/cu.usbserial*`, or `/dev/cu.SLAB_USBtoUART` depending on the USB–serial chip.
- Terminal: `ls /dev/cu.*` before and after plugging the board in; the new name is usually your port.

### Set Pymakr / `pymakr.conf`

Edit `pymakr_project/pymakr.conf` and set `"address"` to your port, for example:

**Windows example**

```json
"address": "COM5"
```

**macOS example**

```json
"address": "/dev/cu.usbmodem1234561"
```

Other keys (defaults may vary by Pymakr version):

- `"sync_folder"` — Often left empty to sync the opened project folder; follow Pymakr’s UI if your version expects a path.
- `"open_on_start"` — Whether to open the terminal when the project loads.
- `"ctrl_c_on_connect"` — Send Ctrl+C on connect to stop a running script and reach the REPL (useful for debugging).

Reconnect USB after driver changes. Only **one** application should use the serial port at a time (close Thonny, other REPLs, or second VS Code windows using the same port).

---

## Open the project and upload (sync) code

1. **Clone** this repository and **checkout** the correct lab branch.
2. In VS Code: **File → Open Folder** and select **`pymakr_project`** (recommended).
3. Open the Pymakr sidebar / panel and **select the project** if prompted.
4. Confirm the **device address** matches `pymakr.conf` or the Pymakr device list.
5. Use **Upload** / **Sync** (wording depends on Pymakr version) to copy project files to the board filesystem.

After sync, **reset** the board (button or unplug/replug). You should see behavior defined by that branch’s `main.py` / `main_rtos.py`.

If your instructor uses a different entry file name on device, follow their naming rules; the default MicroPython boot sequence looks for `main.py` in the root of the filesystem.

---

## Debugging

### Serial output (`print`)

Use `print(...)` in your code; output appears in the **Pymakr terminal** / **REPL** when connected.

### Stop a runaway loop

- In the REPL / terminal: **Ctrl+C** (Windows and macOS in VS Code) to interrupt the running script and return to `>>>`.
- If the board prints too fast to enter raw REPL or sync, see [Troubleshooting](#troubleshooting).

### Soft reset

Many workflows offer **soft reset** so the interpreter restarts and runs `main.py` again without unplugging USB.

### REPL experiments

You can import modules manually:

```python
import main_rtos
```

Use this to isolate errors after upload. Remember: importing may start side effects depending on how the module is written; for this template, the event loop starts from the code guarded at the bottom of `main_rtos.py` when run as the main script.

### `mpremote` (optional CLI mirror)

If you prefer the command line, `mpremote` can copy files similarly to Pymakr (install with `pip`). Example (adjust port and paths):

```bash
python3 -m pip install --user mpremote
mpremote connect /dev/cu.usbmodemXXXX fs cp main_rtos.py :main_rtos.py
```

On Windows use `COM5` style addresses as `mpremote` expects. This is optional; the course may standardize on Pymakr only.

---

## Troubleshooting

| Symptom | What to try |
|--------|-------------|
| **Port busy / access denied** | Close Thonny, Arduino Serial Monitor, other VS Code terminals, and any other tool using the COM/tty port. Unplug and replug USB. |
| **Wrong port** | Re-check Device Manager or `/dev/cu.*`; try another cable or USB port. |
| **Upload fails / raw REPL** | Enable `ctrl_c_on_connect` in `pymakr.conf`; manually open REPL and press Ctrl+C to stop `main.py`; try soft reset; retry sync. |
| **Board spamming errors on boot** | Connect REPL, Ctrl+C, then replace `main.py` temporarily with a no-op loop so you can sync again (instructor may give exact steps). |
| **NeoPixel / LED wrong** | If not using OhStem `pins`/`led_strip`, verify fallback GPIO numbers in `main_rtos.py` match your schematic. |
| **Import errors** | Confirm all files for that lab were synced and that you are on the correct **branch**. |

---

## OhStem vs this workflow

- **OhStem app:** block coding and upload; generated code is MicroPython.
- **This repo:** you edit real `.py` files, use Git branches per lab, and upload with **Pymakr** (or `mpremote`). Behavior should match the course hardware as long as firmware and pin mappings are correct.

---

## License and course use

Use and adapt this documentation for your class as needed. For hardware-specific pin maps and lab rubrics, follow your instructor’s materials.
