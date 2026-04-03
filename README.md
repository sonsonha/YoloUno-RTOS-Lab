# Yolouno-MicroPython (OhStem-compatible starter)

Mục tiêu: tạo sẵn một project MicroPython đơn giản cho `Yolo UNO` để bạn nạp qua VSCode (extension dùng `mpremote`) thay vì kéo-thả trên OhStem App.

## 1) Nội dung chính

- `main_rtos.py`: ví dụ RTOS/async blink cho Yolo UNO (blink LED + đổi NeoPixel song song).
- `main.py`: bản blink NeoPixel đơn giản (fallback máy khác).

Bạn có thể đổi chân trong code nếu cần:

- `NEO_PIN` (NeoPixel RGB onboard, mặc định thử `45`)
- `LED_PIN` (LED đơn fallback, mặc định thử `48`)

## 2) Cách nạp qua VSCode (mpremote)

Phần lớn extension “MicroPython uploader” cho ESP32 thực chất dùng `mpremote`.

1. Cắm `Yolo UNO` qua USB.
2. Tìm cổng serial:
   - macOS: xem thường sẽ là `/dev/cu.usbmodem*` hoặc `/dev/cu.usbserial*`
3. Cài `mpremote`:
   ```bash
   python3 -m pip install --user mpremote
   ```
4. Upload (upload `main_rtos.py` lên device thành `main.py`):
   - Xác định đúng cổng serial (tránh dùng `XXXX`):
     ```bash
     mpremote devs
     ```
   ```bash
   mpremote connect /dev/cu.usbmodem11101 fs cp main_rtos.py :main.py
   ```
   - Nếu báo lỗi “failed to access … (it may be in use by another program)”:
     1. Đóng mọi cửa sổ/REPL/serial monitor đang mở (uPyCraft/Thonny/Arduino IDE/VSCode MPRemote).
     2. Tắt mọi phiên `mpremote connect` đang chạy.
     3. Rút cắm lại `Yolo UNO` và chạy lại lệnh.

   - Nếu báo lỗi “could not enter raw repl” (thường do firmware đang chạy và spam output):
     dùng `resume` để tắt auto soft-reset khi vào raw REPL:
     ```bash
     mpremote connect /dev/cu.usbmodem11101 resume fs cp main_rtos.py :main.py
     ```

   - Nếu vẫn lỗi “could not enter raw repl”, kiểm tra bo có đang vào được MicroPython REPL không:
     ```bash
     mpremote connect /dev/cu.usbmodem11101 repl
     ```
     Bạn gửi mình 10 dòng đầu output (đặc biệt có/không có chữ `Connected to MicroPython` và prompt `>>>`).

## 4) Cứu hộ khi board đang spam (không vào được raw repl để upload)

Trường hợp board đang chạy chương trình cũ và in ra quá nhiều (ví dụ lỗi I2C liên tục) khiến `mpremote fs cp` không vào được raw REPL.

Làm như sau:
1. Mở REPL:
   ```bash
   mpremote connect /dev/cu.usbmodem11101 repl
   ```
2. Nhấn `Ctrl+C` vài lần để dừng chương trình đang chạy và cố gắng quay lại prompt `>>>`.
3. Gõ lệnh sau trong REPL để ghi `main.py` thật “ngủ” (không truy I2C):
   ```python
   open('main.py','w').write("while True:\n  pass\n")
   import machine
   machine.reset()
   ```
4. Sau khi board reset xong, chạy lại upload:
   ```bash
   mpremote connect /dev/cu.usbmodem11101 resume fs cp main_rtos.py :main.py
   ```

Sau đó reset board hoặc ngắt/cắm lại để chạy `main.py`.

## 3) Để khớp 100% “OhStem app -> xem code”

Hiện web docs công khai không đưa thẳng đoạn MicroPython đúng y hệt “code view” của app (đặc biệt các thư viện mở rộng như Camera AI).

Nếu bạn dán giúp mình đoạn code “xem code” của OhStem cho một chương trình cụ thể (ví dụ: bài “Bật tắt đèn LED trên board”), mình sẽ chỉnh `main.py` để khớp cú pháp/tên hàm 1:1.

