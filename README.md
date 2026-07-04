# Kỳ Anh Studio — Design Digital

Toàn bộ website, landing page và công cụ nội bộ của Kỳ Anh Studio trong một thư mục.

## Cấu trúc

```
kyanh-studio/
├── index.html                  # Trang chủ (Task 4 — đang xây)
├── assets/
│   ├── css/design-system.css   # ⭐ Design system dùng chung — sửa 1 chỗ, cả site đổi theo
│   ├── css/main.css            # Style riêng trang chủ
│   ├── js/main.js
│   ├── logo/                   # logo-dark.svg (nền sáng) / logo-light.svg (nền tối)
│   └── images/                 # portfolio / concepts / og
├── pages/
│   ├── booking.html            # Trang đặt lịch (Task 1 — đã có)
│   ├── pricing.html            # Bảng báo giá (Task 4)
│   ├── faq.html                # FAQ (Task 4)
│   ├── feedback.html           # Phản hồi khách (Task 4)
│   └── blog/                   # Blog tin tức (Task 4)
├── landing/
│   └── khuyen-mai-thang-07/    # Landing tháng 7 (Task 2)
├── apps/
│   └── kyanh-reply/            # App trả lời nhanh (Task 3 — đã chạy, Firebase)
└── _template/                  # Template gốc để tham chiếu — KHÔNG deploy/sửa
```

## Mở trong VS Code

1. Mở VS Code → **File → Open Folder** → chọn thư mục `kyanh-studio`.
2. Cài extension **Live Server** (Ritwick Dey) → chuột phải `index.html` → **Open with Live Server** để xem trực tiếp, tự reload khi sửa.

## Quy tắc làm việc

- **Màu, font, nút, form, card, footer** → chỉ định nghĩa trong `assets/css/design-system.css`. Trang nào cũng `<link>` file này. Đừng hardcode màu trong từng trang.
- Token màu: `--ka-cream #FAF9F7` · `--ka-ink #3D3D3D` · `--ka-gold #B8956E` · `--ka-gold-dark #96724A` · dark `#3D3530 → #2A2420`.
- Font: Playfair Display (heading) + Montserrat (body) — nhúng Google Fonts trong `<head>` mỗi trang.
- `_template/` là bản gốc tham chiếu, không sửa, không deploy.

## Deploy lên GitHub Pages

1. Push toàn bộ thư mục này lên repo GitHub (branch `main`).
2. Settings → Pages → Source: **Deploy from a branch** → `main` / `(root)` → Save.
3. URL các trang:
   - Trang chủ: `https://<user>.github.io/<repo>/`
   - Đặt lịch: `.../pages/booking.html`
   - Landing T7: `.../landing/khuyen-mai-thang-07/`
   - App reply: `.../apps/kyanh-reply/`

## App Kỳ Anh Reply (apps/kyanh-reply/)

- Data mẫu lưu trên **Firebase Firestore** (collection `replies`) — update file KHÔNG mất data.
- Trước khi deploy: kiểm tra `window.KA_FIREBASE_CONFIG` trong `index.html` đã có config (apiKey, projectId...). Bản trống config sẽ chạy chế độ máy đơn.
- PIN admin: đặt trong `window.KA_ADMIN_PIN` + Security Rules trên Firebase (2 chỗ phải khớp nhau).
- Chi tiết: xem `apps/kyanh-reply/NOTES.md`.

## Tiến độ task

| # | Task | Trạng thái |
|---|------|-----------|
| 1 | Trang đặt lịch | ✅ Có bản chạy (`pages/booking.html`) |
| 2 | Landing tháng 7 | 🔲 Placeholder |
| 3 | App Kỳ Anh Reply | ✅ Đang vận hành (Firebase) |
| 4 | Website chính (home/pricing/FAQ/blog/feedback) | 🔲 Placeholder |
| 5 | Tối ưu frontend | 🔄 Liên tục |
