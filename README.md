# Yolo UNO — MicroPython trên VSCode (không cần OhStem App)

Môi trường lập trình MicroPython hoàn chỉnh cho **Yolo UNO (ESP32-S3)** sử dụng VSCode + Pymakr, không phụ thuộc OhStem App.

---

## Kiến trúc tổng quan

```
OhStem App (kéo thả)
        ↓  sinh ra
   MicroPython code
        ↓  upload qua USB
   Yolo UNO (ESP32-S3)
        ↓  chạy
   main.py (auto-run khi boot)
```

Bây giờ bạn viết MicroPython trực tiếp trong VSCode và upload bằng **Pymakr** — không cần OhStem App ở bất kỳ bước nào.

---

## 1. Cấu trúc project

```
Yolouno-micropython/
├── pymakr_project/          ← thư mục Pymakr sync lên board
│   ├── main.py              ← file CHÍNH — tự chạy khi board boot
│   ├── lcd_i2c.py           ← driver LCD (thư viện tùy chỉnh)
│   ├── pymakr.json          ← cấu hình Pymakr
│   └── .pymakr-ignore       ← file/folder không upload lên board
├── .vscode/settings.json    ← VSCode: Pymakr chunk settings + stubs
├── .micropython-stubs/      ← MicroPython type stubs (IntelliSense)
└── .gitignore
```

**Quy tắc:** chỉ `main.py` và các `.py` thư viện trong `pymakr_project/` được upload lên board. Mọi thứ còn lại là môi trường dev.

---

## 2. Cài đặt môi trường (một lần)

### 2.1 VSCode Extensions

Cài 2 extension sau trong VSCode:

| Extension | ID |
|---|---|
| Pymakr | `pycom.Pymakr` |
| Pylance | `ms-python.vscode-pylance` |

### 2.2 MicroPython Stubs (IntelliSense cho `machine`, `uasyncio`...)

```bash
pip3 install micropython-esp32-stubs --target .micropython-stubs
```

Sau khi cài, VSCode tự nhận qua `python.analysis.extraPaths` đã cấu hình trong `.vscode/settings.json`.

---

## 3. Workflow phát triển hàng ngày

### Upload code lên board

1. Cắm Yolo UNO qua USB
2. Mở VSCode → tab **Pymakr** ở sidebar trái
3. Click **Connect** trên device `/dev/cu.usbmodem...`
4. Click **Upload** (biểu tượng mũi tên lên) → Pymakr sync `pymakr_project/` lên `/` của board
5. Board tự reset và chạy `main.py`

### Xem output / REPL

- Click **Open terminal** trong Pymakr → mở REPL trực tiếp trên board
- `Ctrl+C` để dừng chương trình đang chạy
- Gõ code Python trực tiếp để test nhanh

### Thêm thư viện tùy chỉnh

1. Đặt file `.py` vào `pymakr_project/`
2. Import bình thường trong `main.py`
3. Upload lại — Pymakr đồng bộ tất cả `.py` trong folder

---

## 4. Xử lý lỗi upload thường gặp

### `SyntaxError: invalid syntax` khi upload

Nguyên nhân: USB transfer quá nhanh gây corrupt data.

Đã fix trong `.vscode/settings.json`:
```json
"adapterOptions": { "chunkSize": 128, "chunkDelay": 200 }
```

Nếu vẫn lỗi, tăng `chunkDelay` lên `300` hoặc `500`.

### Board spam output, không vào được REPL

```bash
# Mở REPL
mpremote connect /dev/cu.usbmodem1234561 repl
# Nhấn Ctrl+C để dừng → gõ:
open('main.py','w').write("pass\n")
import machine; machine.reset()
# Upload lại sau khi board reset xong
```

### Port bị chiếm (`it may be in use`)

- Đóng mọi serial monitor (Thonny, Arduino IDE, terminal mpremote)
- Rút cắm và cắm lại USB

---

## 5. Pin mapping Yolo UNO

| Ký hiệu | GPIO | Ghi chú |
|---|---|---|
| D13 / LED | 48 | LED onboard |
| NeoPixel | 45 | WS2812 RGB onboard |
| Grove I2C (SDA) | 11 | I2C1-I2C4 dùng chung |
| Grove I2C (SCL) | 12 | I2C1-I2C4 dùng chung |
| A1 / Button | 2 | Pull-up nội |
| D2 | 5 | GPIO tự do (tránh GPIO12) |

---

## 6. Labs

| Branch | Nội dung |
|---|---|
| `lab1` | Blink LED + NeoPixel cơ bản |
| `lab2` | GPIO button + I2C DHT20 + LCD 16x2 |
| `lab3` | asyncio Semaphore — button cycle 3 modes |
