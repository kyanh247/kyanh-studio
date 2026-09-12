# KAS Reply | Clipboard

Công cụ nội bộ của Kỳ Anh Studio. Nhân viên mở lên, chạm vào thẻ là nội dung được sao chép,
dán thẳng vào Facebook / Zalo / TikTok cho khách.

Đang chạy tại **https://reply.kyanh.studio**

> ⚠️ Repo này công khai, và GitHub Pages phục vụ **toàn bộ thư mục** — mọi file commit vào
> đây đều tải về được từ địa chỉ trên. Đừng commit mật khẩu, khoá riêng hay thông tin khách.
> Bản sao lưu mẫu (`backup/replies-backup.json`) và các file `.zip` trong `versions/` **cố ý
> không commit** vì lý do đó, xem `.gitignore`.

## App có gì

Hai mục, chuyển qua lại bằng thanh dock dưới đáy màn hình:

- **Trả lời nhanh** — thẻ mẫu trả lời xếp theo danh mục (Gần Đây, Chốt Đơn, Tư Vấn, Bảng Giá,
  Ưu Đãi, All). Mở app là vào thẳng **Gần Đây**; máy nào chưa copy mẫu nào thì vào Chốt Đơn.
  Có ô tìm kiếm xếp theo độ khớp, nút xoá nhanh trong ô tìm, và nút đổi 2 ↔ 3 cột.
- **Concept** — lưới ảnh 2:3 các concept đang bán, kèm link Website / Facebook / TikTok và giá
  cho từng sàn. Lọc theo dạng concept, đổi cỡ ảnh lớn ↔ nhỏ, concept ghim nằm trên đầu.

Thêm vào màn hình chính điện thoại thì chạy như app riêng (toàn màn hình, có icon) — phần này
do `manifest.json` và mấy thẻ `apple-mobile-web-app-*` lo.

## Cấu trúc

```
index.html          ⭐ FILE CHÍNH — toàn bộ app nằm trong một file này
manifest.json       tên + icon khi thêm vào màn hình chính
CNAME               tên miền reply.kyanh.studio
.nojekyll           tắt Jekyll, nếu không GitHub Pages bỏ qua thư mục bắt đầu bằng _
assets/             design-system.css, favicon, logo
backup/             script sao lưu + khôi phục mẫu trả lời
versions/           bản đóng gói .zip của từng mốc ổn định (không commit)
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

Không nằm trong file HTML. Chúng ở **Firestore**, collection `replies`. Mỗi mẫu có `cat` để
biết thuộc danh mục nào; concept là các mẫu `cat = "link-concept"` với thêm ảnh, link và giá.

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

App cũng cất một bản danh sách mẫu trong máy người dùng, nên mở lên là thấy nội dung ngay
rồi mới đồng bộ lại với Firestore.

## Cú pháp mẫu

| Viết trong nội dung | Tác dụng |
|---|---|
| `{{Tên mục}}` | Tạo ô điền, nội dung tự ghép vào tin nhắn |
| `{{*Tên mục}}` | Như trên, giá trị điền vào được in đậm |
| `{{**Tên mục}}` | In đậm nghiêng |
| `[[Concept]] … [[/Concept]]` | Khối lặp, có nút "＋ Thêm concept" |
| `{{#}}` | Số thứ tự tự tăng trong khối lặp |
| `===FB/Zalo===` … `===TikTok===` | Một mẫu chứa nhiều bản, chạm vào thẻ để chọn |

Ba ô **app tự tính**, không hiện ô để gõ mà hiện dòng chỉ để xem:

| Tên mục | Tính từ |
|---|---|
| `{{Còn lại}}` | `Tổng chi phí` trừ `Đã cọc` |
| `{{Giảm %}}` | `Giá gốc` và `Giá khuyến mãi` |
| `{{Giá TikTok}}` | `Giá khuyến mãi`, rút gọn phần nghìn và chèn 🌼 để né kiểm duyệt giá |

Ô nào có chữ "giá", "chi phí", "cọc" hay "tiền" trong tên thì tự chấm hàng nghìn khi gõ:
gõ `5000000` thành `5.000.000`.

## Sao lưu

```bash
python backup/sao-luu.py                 # chụp toàn bộ mẫu ra backup/replies-backup.json
python backup/sao-luu.py --ra <thư mục>  # lưu ra ngoài repo, tên kèm ngày giờ, giữ 12 bản
python backup/khoi-phuc.py               # xem trước mẫu đang thiếu, KHÔNG ghi gì
python backup/khoi-phuc.py --that        # đăng nhập rồi nạp lại các mẫu đã mất
```

Máy của Kỳ Anh có tác vụ Windows `KyAnhReply-SaoLuu` chạy **mỗi Chủ Nhật 12h00**, lưu vào
`Reply\Sao-luu-tu-dong\` — nằm **ngoài repo** nên không lên GitHub.

`khoi-phuc.py` tự chọn bản sao lưu **mới nhất** giữa thư mục sao lưu tự động và bản trong
repo, và cảnh báo nếu bản nó chọn đã cũ hơn 10 ngày. Muốn ép dùng một file cụ thể thì thêm
`--tu <đường dẫn>`.

Script chỉ nạp lại mẫu **đã mất**, không đè lên mẫu đang có — chạy nhầm cũng không làm hỏng
dữ liệu hiện tại. Đổi lại, mẫu bị **sửa hỏng** (chứ không bị xoá) thì script không cứu được.

## Deploy

Push lên nhánh `master` là GitHub Pages tự build, khoảng 1 phút sau bản mới đã nằm trên
`reply.kyanh.studio`.

Máy người dùng thấy chậm hơn một chút: trình duyệt giữ bản cũ tối đa 10 phút
(`Cache-Control: max-age=600`). App tự kiểm tra bản mới lúc mở, mỗi 10 phút, và mỗi lần quay
lại tab — có bản mới thì tự tải lại, trừ khi đang mở hộp thoại hoặc đang gõ dở.
