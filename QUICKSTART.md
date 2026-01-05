# 🚀 Quick Start - Di Cho Tien Loi

Hướng dẫn nhanh để khởi động ứng dụng quản lý thực phẩm và mua sắm.

## 📋 Yêu cầu

- **Backend**: Docker Desktop
- **Frontend**: Flutter SDK 3.10+
- **Ports**: 8000, 5432, 6379, 9000, 9001

---

## 🚀 Khởi động Backend

```bash
# 1. Clone project
git clone https://github.com/your-repo/PTUD_Da-nen-tang.git
cd PTUD_Da-nen-tang

# 2. Tạo file .env (Windows)
copy backend\.env.example backend\.env

# 3. Khởi động Docker
docker-compose up -d

# 4. Kiểm tra: http://localhost:8000/docs
```

⏱️ Chờ ~2 phút để services khởi động.

---

## 📱 Khởi động Frontend

```bash
# 1. Cài đặt dependencies
cd frontend
flutter pub get

# 2. Chạy trên Chrome/Web
flutter run -d chrome

# 3. Hoặc chạy trên Android/iOS
flutter run
```

### Cấu hình API URL

Mở [frontend/lib/config/api_config.dart](frontend/lib/config/api_config.dart):

```dart
// Chrome/Web: http://localhost:8000/api/v1
// Android Emulator: http://10.0.2.2:8000/api/v1  
// Physical Device: http://192.168.1.X:8000/api/v1
static const String baseUrl = 'http://localhost:8000/api/v1';
```

### Cấu hình Groq API Key (Tùy chọn)

Nếu bạn muốn sử dụng tính năng AI chatbot, cần cấu hình Groq API key:

1. **Lấy API key**: Truy cập https://console.groq.com/keys để tạo key miễn phí
2. **Cấu hình trong file**: Mở [frontend/lib/config/api_config.dart](frontend/lib/config/api_config.dart)
3. **Thay thế placeholder**:
   ```dart
   // Thay thế chuỗi rỗng bằng API key của bạn
   static const String groqApiKey = 'gsk_your_actual_api_key_here';
   ```

⚠️ **Lưu ý**: Không commit API key lên git. Chỉ dùng cho development local.

---

## �️ Xử lý lỗi thường gặp

### Backend không chạy

```bash
# Kiểm tra Docker đang chạy
docker ps

# Xem logs
docker-compose logs backend

# Restart services
docker-compose restart
```

### Frontend không kết nối API

1. Kiểm tra backend: http://localhost:8000/healthz
2. Đổi URL trong [api_config.dart](frontend/lib/config/api_config.dart):
   - Android Emulator: `http://10.0.2.2:8000/api/v1`
   - Physical Device: `http://<YOUR_IP>:8000/api/v1` (dùng `ipconfig` để tìm IP)
3. Hot restart Flutter: Press `R`

### Reset toàn bộ

```bash
# Xóa tất cả containers và volumes
docker-compose down -v

# Khởi động lại
docker-compose up -d
```

---

## 📚 Tài liệu

- **API Docs**: http://localhost:8000/docs (khi backend chạy)
- **Backend Guide**: [BACKEND_GUIDE.md](BACKEND_GUIDE.md)
- **Admin Guide**: [ADMIN_GUIDE.md](ADMIN_GUIDE.md)
- **Postman Collection**: [postman/](postman/)

---

## 📝 Lưu ý

- ⚠️ Đổi `SECRET_KEY` và `ADMIN_PASSWORD` trong production
- 🔓 Không cần xác thực email - đăng nhập ngay sau đăng ký
- 🐳 Đảm bảo Docker Desktop đang chạy
- 🤖 Groq API key (optional) cho tính năng AI

**Admin mặc định**: admin / change-this-password

---

**Happy Coding! 🚀**
