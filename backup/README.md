# Sao lưu mẫu trả lời — KAS Reply

Nội dung các mẫu trả lời nằm trên Firebase, **không nằm trong file HTML**.
Thư mục này giữ script sao lưu và khôi phục.

## Nếu mẫu bị mất — cách lấy lại

Mở Terminal tại thư mục `kyanh-studio`, chạy:

```bash
python backup/khoi-phuc.py
```

Lệnh này **chỉ xem trước**: nó in ra đang dùng bản sao lưu nào, sao lưu lúc nào, và những
mẫu đang thiếu — chưa ghi gì lên Firebase, chưa hỏi mật khẩu. Xem thấy đúng rồi thì chạy:

```bash
python backup/khoi-phuc.py --that
```

Lúc này script hỏi **email + mật khẩu quản trị** (tài khoản đã thêm trong Firebase Console)
rồi mới ghi. Chỉ những mẫu **đã mất** được nạp lại; mẫu còn trên Firebase giữ nguyên, không
bị ghi đè — nên chạy nhầm cũng không làm hỏng dữ liệu đang có.

Mẫu bị **sửa hỏng** chứ không bị xoá thì script không cứu được, vì với nó mẫu đó vẫn còn.

## Script lấy bản sao lưu nào

Tự chọn bản **mới nhất** trong hai chỗ:

- `Reply\Sao-luu-tu-dong\` — tác vụ Windows `KyAnhReply-SaoLuu` chạy mỗi Chủ Nhật 12h00,
  nằm ngoài repo, giữ 12 bản gần nhất.
- `backup/replies-backup.json` — bản trong repo, chỉ cập nhật khi chạy tay `sao-luu.py`.

Nếu bản được chọn đã cũ hơn 10 ngày, script cảnh báo ngay trên màn hình: khôi phục bằng bản
cũ nghĩa là **mất hết mẫu thêm sau ngày đó**. Muốn ép dùng một file khác:

```bash
python backup/khoi-phuc.py --tu "F:\...\replies-2026-09-06_1200.json"
```

## Cập nhật bản sao lưu bằng tay

```bash
python backup/sao-luu.py                 # ghi đè backup/replies-backup.json
python backup/sao-luu.py --ra <thư mục>  # lưu ra ngoài repo, tên kèm ngày giờ
```

## Lưu ý

- `replies-backup.json` **không commit** lên GitHub (xem `.gitignore`): repo công khai, ai
  cũng tải được file đó nếu nó nằm trong repo.
- Hai script này không chứa mật khẩu. `apiKey` được đọc từ `index.html` — key đó vốn là
  thông tin công khai, thứ bảo vệ dữ liệu là Firestore Rules.
- Cách ghi cũ bằng `_key` = PIN đã bị Rules chặn từ commit `21f2ef9`, không dùng được nữa.
