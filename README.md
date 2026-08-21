# Kỳ Anh Reply

Công cụ trả lời nhanh dùng nội bộ của Kỳ Anh Studio. Nhân viên mở lên, chạm vào thẻ là
nội dung được sao chép, dán thẳng vào Facebook / Zalo / TikTok cho khách.

Đang chạy tại **https://reply.kyanh.studio**

> ⚠️ Repo này công khai, và GitHub Pages phục vụ **toàn bộ thư mục** — mọi file ở đây đều
> tải về được từ địa chỉ trên. Đừng commit mật khẩu, khoá riêng hay thông tin khách hàng.

## Cấu trúc

```
index.html          ⭐ FILE CHÍNH — toàn bộ app nằm trong một file này
CNAME               tên miền reply.kyanh.studio
.nojekyll           tắt Jekyll, nếu không GitHub Pages bỏ qua thư mục bắt đầu bằng _
assets/             design-system.css, favicon, logo
backup/             script sao lưu + khôi phục mẫu trả lời
versions/           bản đóng gói .zip của từng mốc ổn định
apps/kyanh-reply/   bản cũ — giữ nguyên theo quy ước, không xoá
reply/              trang chuyển hướng ngắn /reply/
_template/          template gốc để tham chiếu, không deploy
```

**Sửa tính năng thì sửa `index.html` ở gốc.** Bản trong `apps/kyanh-reply/` là bản cũ giữ
lại, không phải bản đang chạy.

App là **một file HTML tĩnh** — không có bước build, không cần cài gì. Mở ra là chạy.

## Chạy thử ở máy

```bash
python -m http.server 8765
```

Rồi mở http://localhost:8765

**Đừng mở bằng `file:///`** — qua giao thức đó Firebase không nạp được dữ liệu, app hiện
0 mẫu và rất dễ tưởng là hỏng.

Sửa `index.html` xong chỉ cần F5, không phải khởi động lại server.

## Dữ liệu mẫu trả lời

Không nằm trong file HTML. Chúng ở **Firestore**, collection `replies`.

- `SEED_ITEMS` trong `index.html` chỉ là dữ liệu khởi tạo cho lần cài mới. Sửa nó **không**
  đổi được mẫu thật.
- Thêm / sửa / xoá mẫu thì làm ngay trong app sau khi đăng nhập.
- Sửa dữ liệu là **mọi máy thấy ngay** — không có bước "thử ở local" như khi sửa code.

Đọc được không cần đăng nhập, tiện để đối chiếu:

```bash
curl -s "https://firestore.googleapis.com/v1/projects/ky-anh-studio---reply-d43ff/databases/(default)/documents/replies?pageSize=300"
```

Ghi thì phải đăng nhập bằng email quản trị — danh sách email đặt trong Firestore Rules
trên Firebase Console, cố ý không ghi ra file nào trong repo.

## Sao lưu

```bash
python backup/sao-luu.py          # chụp lại toàn bộ mẫu ra replies-backup.json
python backup/khoi-phuc.py        # xem trước những mẫu đang thiếu, KHÔNG ghi gì
python backup/khoi-phuc.py --that # đăng nhập rồi nạp lại các mẫu đã mất
```

`khoi-phuc.py` chỉ nạp lại mẫu **đã mất**, không đè lên mẫu đang có — chạy nhầm cũng không
làm hỏng dữ liệu hiện tại.

`replies-backup.json` là ảnh chụp tại một thời điểm, **không tự cập nhật**. Thêm nhiều mẫu
mới thì nhớ chạy lại `sao-luu.py`.

## Cú pháp mẫu

| Viết trong nội dung | Tác dụng |
|---|---|
| `{{Tên mục}}` | Tạo ô điền, nội dung tự ghép vào tin nhắn |
| `[[Concept]] … [[/Concept]]` | Khối lặp, có nút "＋ Thêm concept" |
| `{{#}}` | Số thứ tự tự tăng trong khối lặp |
| `===FB/Zalo===` … `===TikTok===` | Một mẫu chứa nhiều bản, chạm vào thẻ để chọn |

## Giao diện

Tông kem + vàng đồng, font Playfair Display (tiêu đề) + Montserrat (nội dung). Token màu
định nghĩa trong `assets/css/design-system.css` (`--ka-*`) — dùng biến, đừng ghi cứng mã màu
trong từng trang.

## Deploy

Push lên nhánh `master` là GitHub Pages tự build, khoảng 1 phút sau là bản mới lên
`reply.kyanh.studio`. App tự tải lại khi phát hiện bản mới, nhân viên không phải làm gì.
