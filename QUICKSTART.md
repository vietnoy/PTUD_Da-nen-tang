# 🚀 Di Cho Tien Loi - Quick Start Guide

Hướng dẫn nhanh để khởi động dự án "Đi Chợ Tiện Lợi" - ứng dụng quản lý thực phẩm và mua sắm cho gia đình.

## 📋 Mục lục

1. [Tổng quan](#tổng-quan)
2. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
3. [Cài đặt nhanh](#cài-đặt-nhanh)
4. [Chạy Backend](#chạy-backend)
5. [Chạy Frontend](#chạy-frontend)
6. [Sử dụng API](#sử-dụng-api)
7. [Xử lý sự cố](#xử-lý-sự-cố)

---

## 🎯 Tổng quan

**Di Cho Tien Loi** là ứng dụng đa nền tảng giúp các hộ gia đình:
- 📦 Quản lý tủ lạnh và kho thực phẩm
- 🛒 Tạo và chia sẻ danh sách mua sắm
- 🍽️ Lên kế hoạch bữa ăn
- 👥 Phối hợp trong nhóm/gia đình

### Kiến trúc:
- **Backend**: FastAPI + PostgreSQL + Redis + MinIO + Celery
- **Frontend**: Flutter (cross-platform)
- **Deployment**: Docker & Docker Compose

---

## 💻 Yêu cầu hệ thống

### Backend:
- Docker Desktop (hoặc Docker Engine + Docker Compose)
- Git
- 4GB RAM trở lên
- Port 8000, 5432, 6379, 9000, 9001 phải available

### Frontend:
- Flutter SDK 3.10.4 trở lên
- Dart SDK
- Android Studio / Xcode (cho mobile)
- Chrome / Edge (cho web)

---

## ⚡ Cài đặt nhanh

### 1. Clone Repository

```bash
git clone https://github.com/your-repo/PTUD_Da-nen-tang.git
cd PTUD_Da-nen-tang
```

### 2. Cấu hình Backend

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo file .env từ template (nếu chưa có)
# Trên Windows:
copy .env.example .env

# Trên Linux/Mac:
cp .env.example .env
```

**Lưu ý**: Mở file `.env` và cập nhật các thông tin cần thiết (đặc biệt là SMTP cho email).

### 3. Khởi động Backend với Docker

```bash
# Quay về thư mục gốc
cd ..

# Build và start tất cả services
docker-compose up --build

# Hoặc chạy ở chế độ background:
docker-compose up -d --build
```

Chờ khoảng 2-3 phút để các services khởi động hoàn toàn.

### 4. Kiểm tra Backend

Mở trình duyệt và truy cập:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/healthz
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

### 5. Cài đặt Frontend

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies
flutter pub get

# Kiểm tra Flutter setup
flutter doctor
```

---

## 🔧 Chạy Backend

### Sử dụng Docker (Khuyến nghị)

```bash
# Start tất cả services
docker-compose up

# Start ở background
docker-compose up -d

# Xem logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Xóa volumes (reset database)
docker-compose down -v
```

### Các Services bao gồm:

| Service | Port | Mô tả |
|---------|------|-------|
| Backend API | 8000 | FastAPI server |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache & message broker |
| MinIO | 9000, 9001 | Object storage |
| Celery Worker | - | Background tasks |
| Celery Beat | - | Scheduled tasks |

### Chạy Migration (nếu cần)

```bash
# Vào container backend
docker-compose exec backend bash

# Chạy migrations
alembic upgrade head

# Thoát container
exit
```

### Reset Database

```bash
# Dừng services và xóa volumes
docker-compose down -v

# Khởi động lại
docker-compose up --build
```

---

## 📱 Chạy Frontend

### Trên Web (Chrome/Edge)

```bash
cd frontend
flutter run -d chrome
```

### Trên Android Emulator

```bash
# Đảm bảo emulator đã chạy
flutter emulators --launch <emulator_id>

# Run app
flutter run -d <device_id>
```

### Trên iOS Simulator (chỉ macOS)

```bash
# Mở simulator
open -a Simulator

# Run app
flutter run -d ios
```

### Build APK (Android)

```bash
flutter build apk --release

# File APK sẽ ở: build/app/outputs/flutter-apk/app-release.apk
```

### Cấu hình API URL

Mở `frontend/lib/services/api_client.dart` và cập nhật:

```dart
// Cho Android Emulator
static const String baseUrl = 'http://10.0.2.2:8000/api/v1';

// Cho iOS Simulator / Real device
static const String baseUrl = 'http://localhost:8000/api/v1';
// hoặc sử dụng IP thực của máy: http://192.168.1.x:8000/api/v1
```

---

## 🔌 Sử dụng API

### 1. Đăng ký tài khoản

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "Nguyen Van A",
    "user_name": "nguyenvana"
  }'
```

**Lưu ý**: Sau khi đăng ký, người dùng có thể đăng nhập ngay mà không cần xác thực email (đã bỏ phần xác thực Gmail).

### 2. Đăng nhập

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Response sẽ trả về `accessToken` và `refreshToken`.

### 3. Gọi API với Authentication

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Import Postman Collection

File Postman collection có sẵn tại: `postman/Di cho tien loi API.postman_collection.json`

**Cách import:**
1. Mở Postman
2. Click **Import**
3. Chọn file JSON ở thư mục `postman/`
4. Sử dụng các request mẫu có sẵn

---

## 🛠️ Xử lý sự cố

### Backend không khởi động

**Vấn đề**: Port đã được sử dụng
```bash
# Kiểm tra port đang dùng
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Dừng process hoặc thay đổi port trong docker-compose.yml
```

**Vấn đề**: Database connection failed
```bash
# Xem logs của PostgreSQL
docker-compose logs db

# Restart database
docker-compose restart db
```

### Frontend không kết nối được API

**Giải pháp**:
1. Kiểm tra backend đã chạy: http://localhost:8000/healthz
2. Kiểm tra URL trong `api_client.dart`:
   - Android Emulator: `http://10.0.2.2:8000`
   - iOS Simulator: `http://localhost:8000`
   - Real device: `http://<YOUR_IP>:8000` (tìm IP bằng `ipconfig` hoặc `ifconfig`)
3. Tắt firewall hoặc cho phép port 8000

### Migration lỗi

```bash
# Xem trạng thái migrations
docker-compose exec backend alembic current

# Reset migrations (cẩn thận - mất dữ liệu!)
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head

# Hoặc xóa database và tạo lại
docker-compose down -v
docker-compose up --build
```

### Xóa cache Flutter

```bash
flutter clean
flutter pub get
flutter pub upgrade
```

### Logs debugging

```bash
# Xem logs backend
docker-compose logs -f backend

# Xem logs tất cả services
docker-compose logs -f

# Xem logs Celery worker
docker-compose logs -f worker
```

---

## 📚 Tài liệu thêm

- **Backend chi tiết**: [BACKEND_GUIDE.md](BACKEND_GUIDE.md)
- **API Documentation**: http://localhost:8000/docs (khi backend đang chạy)
- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **Data Model**: [docs/data-model.md](docs/data-model.md)

---

## 🎯 Next Steps

Sau khi hoàn thành quick start:

1. ✅ Đọc [BACKEND_GUIDE.md](BACKEND_GUIDE.md) để hiểu chi tiết backend
2. ✅ Khám phá API qua Swagger UI: http://localhost:8000/docs
3. ✅ Xem Postman collection để test API
4. ✅ Tùy chỉnh UI/UX của Flutter app
5. ✅ Thêm features mới theo yêu cầu

---

## 🤝 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra [Xử lý sự cố](#xử-lý-sự-cố) ở trên
2. Xem logs: `docker-compose logs -f`
3. Kiểm tra [Issues](https://github.com/your-repo/issues) trên GitHub

---

## 📝 Lưu ý quan trọng

- ⚠️ **Đã bỏ xác thực Gmail**: Người dùng có thể đăng nhập ngay sau khi đăng ký
- 🔒 **Security**: Đổi mật khẩu mặc định trong production
- 💾 **Backup**: Định kỳ backup database PostgreSQL
- 🐳 **Docker**: Đảm bảo Docker Desktop đang chạy trước khi start services

---

**Happy Coding! 🚀**
