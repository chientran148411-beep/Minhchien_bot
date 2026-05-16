
# Discord Shop Bot + SePay QR

## Chức năng
- Tạo danh mục
- Thêm / sửa / xóa sản phẩm
- Tạo QR thanh toán
- Kiểm tra giao dịch qua SePay webhook
- Gửi key tự động khi thanh toán thành công
- Admin panel bằng button Discord

## Công nghệ
- Node.js
- discord.js v14
- express
- sqlite3

## Cài đặt
```bash
npm install
node index.js
```

## ENV
Tạo file `.env`
```env
DISCORD_TOKEN=YOUR_TOKEN
CLIENT_ID=YOUR_CLIENT_ID
GUILD_ID=YOUR_GUILD_ID

BANK_NAME=MBBANK
BANK_NUMBER=0123456789
ACCOUNT_NAME=SHOP BOT

SEPAY_API_KEY=YOUR_SEPAY_KEY
BASE_URL=https://your-domain.com
```

## Webhook
Trỏ webhook SePay về:
```
https://your-domain.com/webhook/sepay
```
