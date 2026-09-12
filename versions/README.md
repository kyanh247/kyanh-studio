# Các phiên bản đã đóng gói

Mỗi file `.zip` ở đây là một bản hoàn chỉnh của app tại một thời điểm:
code + logo + toàn bộ mẫu trả lời. Dùng để quay về khi bản mới có trục trặc.

> Các file `.zip` **không commit** lên GitHub (xem `.gitignore`) — bên trong có bản sao
> toàn bộ mẫu trả lời, mà repo này thì công khai. Chúng chỉ nằm trên máy Kỳ Anh.

| Phiên bản | Ngày | Ghi chú |
|---|---|---|
| `kyanh-reply-v1.0.0.zip` | 17/08/2026 | Mốc ổn định đầu tiên. Có đăng nhập email/mật khẩu, 70 mẫu. |

Chi tiết từng bản nằm trong file `GHI-CHU.md` bên trong mỗi zip.

## Quay về một bản cũ

1. Giải nén file zip của bản đó ra một thư mục tạm
2. Chép đè `index.html` và thư mục `assets/` vào thư mục gốc của repo
3. `git commit` rồi `git push` — vài phút sau `reply.kyanh.studio` sẽ chạy bản đó
4. Nếu cần khôi phục cả mẫu trả lời: chạy `python backup/khoi-phuc.py` (xem trước) rồi
   `python backup/khoi-phuc.py --that` (nạp thật). Script tự lấy bản sao lưu mới nhất;
   muốn dùng đúng bản trong zip thì thêm `--tu <đường dẫn tới replies-backup.json>`

## Xem code của một bản cũ mà không cần tải zip

Mỗi bản đều được đánh dấu trong Git, xem trực tiếp trên GitHub:

    https://github.com/kyanh247/kyanh-studio/tree/v1.0.0

## Đóng gói bản mới

Khi chốt một mốc mới, chạy `python backup/sao-luu.py` để lấy mẫu mới nhất,
rồi gói `index.html` + `assets/favicon/` + `backup/` lại thành
`kyanh-reply-vX.Y.Z.zip` và thêm một dòng vào bảng trên.
