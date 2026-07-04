# Kỳ Anh Reply — Ghi chú vận hành

## Cấu hình (trong index.html, khối "KHỐI CẤU HÌNH")
- `window.KA_ADMIN_PIN` — mã PIN admin. PHẢI khớp với `_key` trong Security Rules trên Firebase.
- `window.KA_FIREBASE_CONFIG` — dán từ Firebase Console (Project settings → Your apps → Web).
  ⚠️ Trước mỗi lần deploy: kiểm tra config còn trong file. Bản trống config = chế độ máy đơn (không đồng bộ).

## Firebase
- Project: console.firebase.google.com → project của studio
- Data: Firestore → collection `replies`
- Rules: tab Rules — allow read tất cả, allow write khi `_key` == PIN

## Data an toàn
- Update file HTML KHÔNG mất data (data nằm trên Firebase).
- Đừng đổi `projectId` trong config và tên collection `replies`.

## Cú pháp template điền nhanh
- `{{Tên mục}}` → ô điền, tự ghép vào tin nhắn
- `[[Concept]] ... [[/Concept]]` → khối lặp, có nút "＋ Thêm concept"
- `{{#}}` → số thứ tự tự tăng trong khối lặp
