# YoloUno MicroPython Labs (main branch handbook)

Tai lieu nay la huong dan chung cho toan bo project tren branch `main`: setup, nap code bang phím tat (`Cmd + Shift + B` / `Ctrl + Shift + B`), debug khi nap loi, gioi thieu cac branch lab, va cac luu y khi day/hoc.

## 1) Tong quan repository

- Board: **YoloUno** (ESP32-S3, chay MicroPython firmware).
- Muc tieu: code truc tiep bang Python trong VS Code, khong can keo-tha block.
- Thu muc chinh:
  - `pymakr_project/`: source duoc nap len board.
  - `.vscode/tasks.json`: build tasks de nap nhanh bang phim tat.
  - `README.md`: tai lieu huong dan.

## 2) Cac branch lab

- `lab1`: LED + NeoPixel, async/cooperative multitask co ban.
- `lab2`: GPIO + I2C (DHT20/LCD), doc cam bien va hien thi.
- `lab3`: semaphore/mode switching, mo rong tu lab2.
- `main`: branch huong dan tong hop + tai lieu dung chung.

Khi hoc/giang day, luon xac nhan dang dung dung branch truoc khi nap:

```bash
git branch --show-current
```

## 3) Dieu kien can thiet

1. Cap USB co truyen data (khong chi sac).
2. Board da co firmware MicroPython phu hop.
3. Cai VS Code.
4. Cai Python 3.
5. Cai extension VS Code:
   - `ms-python.python`
   - `ms-python.vscode-pylance`
   - `pycom.Pymakr` (khuyen nghi de mo REPL/serial)
6. Cai `mpremote`:

```bash
python -m pip install mpremote
```

## 4) Setup de bam Cmd/Ctrl + Shift + B nap duoc code

Project da co san build task. Ban chi can:

1. Mo folder project trong VS Code (`Yolouno-micropython` hoac `pymakr_project`).
2. Cam board YoloUno qua USB.
3. Dong tat ca cua so Serial Monitor/REPL dang mo.
4. Bam:
   - **macOS:** `Cmd + Shift + B`
   - **Windows:** `Ctrl + Shift + B`
5. Chon task upload (`Upload via mpremote` hoac `Upload Lab1 via mpremote`, tuy branch).
6. Nhap serial port:
   - macOS: vi du `/dev/cu.usbmodem1234561`
   - Windows: vi du `COM3`, `COM4`
7. Cho task chay xong, board tu reset va chay `main.py`.

## 5) Cach tim serial port

- **macOS**: thuong la `/dev/cu.usbmodem...` hoac `/dev/cu.usbserial...`
- **Windows**: vao Device Manager -> `Ports (COM & LPT)` de lay `COMx`

Neu khong chac port, rut cam lai board va xem cong nao moi xuat hien.

## 6) Debug khi khong nap duoc

### A. Loi `ValueError: odd-length string` (Pymakr)

- Nguyen nhan thuong gap: upload folder qua Pymakr bi loi serialize.
- Cach xu ly: dung build task (`Cmd/Ctrl + Shift + B`) voi `mpremote`.

### B. Loi `failed to access ... it may be in use by another program`

- Dang co app khac giu cong serial.
- Dong Pymakr terminal, Arduino Serial Monitor, Thonny, session mpremote cu.
- Rut/cam lai USB roi nap lai.

### C. Bam Cmd/Ctrl + Shift + B nhung khong thay task upload

- Ban dang mo sai folder/workspace.
- Dung `File -> Open Folder` va mo lai `Yolouno-micropython` hoac `pymakr_project`.
- Reload VS Code window (`Developer: Reload Window`).

### D. VS Code bao `Import "machine" / "uasyncio" could not be resolved`

- Day la canh bao Pylance tren may tinh, khong phai loi firmware tren board.
- Neu code nap va chay duoc tren board thi co the bo qua canh bao nay.

### E. LCD hien thi sai noi dung (vi du con code lab cu)

- Kiem tra task upload co copy day du file phu thuoc (`main.py`, `main_rtos.py`, `lcd_i2c.py` neu can).
- Nap lai bang task full upload thay vi `main.py only`.

## 7) Quy trinh de xuat cho sinh vien (standard classroom flow)

1. `git checkout <lab-branch>`
2. Mo dung folder project.
3. Cam board.
4. Bam `Cmd/Ctrl + Shift + B`.
5. Chon upload task.
6. Nhap dung port.
7. Kiem tra output qua `Open REPL`.

## 8) Luu y quan trong

- Chi mot chuong trinh duoc dung serial port tai mot thoi diem.
- Luon xac nhan branch truoc khi nap.
- Neu task co prompt port, nhap dung OS format (`/dev/cu...` vs `COMx`).
- Uu tien upload task bang `mpremote` de on dinh hon upload folder trong Pymakr.
- Truoc gio hoc, nen test nhanh 1 lan tren ca macOS va Windows.
