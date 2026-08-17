# Sao lưu mẫu trả lời — Kỳ Anh Reply

Nội dung các mẫu trả lời nằm trên Firebase, **không nằm trong file HTML**.
Thư mục này giữ bản sao phòng khi dữ liệu bị xoá.

## Nếu mẫu bị mất — cách lấy lại

Mở Terminal tại thư mục `kyanh-studio`, chạy:

```bash
python backup/khoi-phuc.py
```

Lệnh này **chỉ xem trước**, liệt kê những mẫu đang thiếu, chưa ghi gì lên Firebase.
Xem thấy đúng rồi thì chạy tiếp:

```bash
python backup/khoi-phuc.py --that
```

Chỉ những mẫu **đã mất** mới được nạp lại. Mẫu nào còn trên Firebase thì giữ nguyên,
không bị ghi đè — nên chạy nhầm cũng không làm hỏng dữ liệu đang có.

## Cập nhật bản sao lưu

`replies-backup.json` là ảnh chụp tại thời điểm sao lưu, **không tự cập nhật**.
Thêm nhiều mẫu mới thì nhớ sao lưu lại, nếu không bản cũ sẽ thiếu mẫu mới.

## Lưu ý

- Nếu sau này chuyển sang đăng nhập bằng email/mật khẩu (Firebase Auth),
  script khôi phục cần sửa lại để đăng nhập trước khi ghi.
- `PIN` trong `khoi-phuc.py` phải khớp `KA_ADMIN_PIN` trong `index.html`.
