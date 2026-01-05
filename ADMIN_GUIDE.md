# Admin Panel Guide

## Tổng quan

Admin panel đã được tích hợp vào ứng dụng "Di Cho Tien Loi" với các chức năng quản lý:
- **Users**: Quản lý tài khoản người dùng
- **Units**: Quản lý đơn vị đo lường
- **Categories**: Quản lý danh mục thực phẩm

## Cấu hình Backend

### 1. Thêm thông tin đăng nhập Admin vào file .env

Tạo hoặc cập nhật file `.env` trong thư mục `backend/`:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

**LƯU Ý**: Trong môi trường production, vui lòng thay đổi username và password mặc định!

### 2. API Endpoints

Admin API được mount tại `/api/v1/admin`:

#### Authentication
- `POST /api/v1/admin/login` - Đăng nhập admin

#### User Management
- `GET /api/v1/admin/users` - Lấy danh sách users
- `GET /api/v1/admin/users/{user_id}` - Lấy thông tin user
- `POST /api/v1/admin/users` - Tạo user mới
- `PUT /api/v1/admin/users/{user_id}` - Cập nhật user
- `DELETE /api/v1/admin/users/{user_id}` - Xóa user

#### Unit Management
- `GET /api/v1/admin/units` - Lấy danh sách units
- `GET /api/v1/admin/units/{unit_id}` - Lấy thông tin unit
- `POST /api/v1/admin/units` - Tạo unit mới
- `PUT /api/v1/admin/units/{unit_id}` - Cập nhật unit
- `DELETE /api/v1/admin/units/{unit_id}` - Xóa unit

#### Category Management
- `GET /api/v1/admin/categories` - Lấy danh sách categories
- `GET /api/v1/admin/categories/{category_id}` - Lấy thông tin category
- `POST /api/v1/admin/categories` - Tạo category mới
- `PUT /api/v1/admin/categories/{category_id}` - Cập nhật category
- `DELETE /api/v1/admin/categories/{category_id}` - Xóa category

## Cấu hình Frontend

### 1. Truy cập Admin Panel

Từ màn hình đăng nhập của ứng dụng, click vào link "Admin Panel" ở phía dưới.

### 2. Đăng nhập

Sử dụng username và password đã cấu hình trong file `.env`:
- Username: `admin` (mặc định)
- Password: `admin123` (mặc định)

### 3. Giao diện quản lý

Sau khi đăng nhập thành công, bạn sẽ thấy dashboard với 3 tab:
- **Users**: Quản lý người dùng
- **Units**: Quản lý đơn vị
- **Categories**: Quản lý danh mục

## Các chức năng chính

### Quản lý Users

**Thêm User mới:**
1. Click nút "Thêm User"
2. Điền thông tin: Email, Tên, Username, Password
3. Chọn trạng thái: Activated, Verified
4. Click "Thêm"

**Chỉnh sửa User:**
1. Click icon "Edit" bên cạnh user muốn chỉnh sửa
2. Cập nhật thông tin cần thiết
3. Để trống password nếu không muốn đổi
4. Click "Cập nhật"

**Xóa User:**
1. Click icon "Delete" bên cạnh user muốn xóa
2. Xác nhận xóa

### Quản lý Units

**Thêm Unit mới:**
1. Click nút "Thêm Unit"
2. Điền thông tin:
   - Tên đơn vị (ví dụ: kg, lít, cái)
   - Loại: Weight, Volume, Count, hoặc Length
   - Convert to base: Hệ số chuyển đổi (1.0 cho đơn vị cơ bản)
   - Is Base Unit: Đánh dấu nếu là đơn vị cơ bản
3. Click "Thêm"

**Chỉnh sửa Unit:**
1. Click icon "Edit" bên cạnh unit muốn chỉnh sửa
2. Cập nhật thông tin cần thiết
3. Click "Cập nhật"

**Xóa Unit:**
1. Click icon "Delete" bên cạnh unit muốn xóa
2. Xác nhận xóa

### Quản lý Categories

**Thêm Category mới:**
1. Click nút "Thêm Category"
2. Điền thông tin:
   - Tên danh mục (ví dụ: Rau củ, Thịt cá, Trái cây)
   - Mô tả (tùy chọn)
3. Click "Thêm"

**Chỉnh sửa Category:**
1. Click icon "Edit" bên cạnh category muốn chỉnh sửa
2. Cập nhật thông tin cần thiết
3. Click "Cập nhật"

**Xóa Category:**
1. Click icon "Delete" bên cạnh category muốn xóa
2. Xác nhận xóa

## Bảo mật

### Khuyến nghị bảo mật:

1. **Thay đổi mật khẩu mặc định** trong file `.env`
2. **Không commit** file `.env` vào Git
3. **Sử dụng HTTPS** khi deploy production
4. **Giới hạn IP** có thể truy cập admin panel trong production
5. **Thêm rate limiting** cho admin endpoints
6. **Sử dụng mật khẩu mạnh** (ít nhất 12 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt)

### Ví dụ mật khẩu mạnh:

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=MyStr0ng@dminP@ssw0rd!2024
```

## Khắc phục sự cố

### Không thể đăng nhập

1. Kiểm tra file `.env` có đúng cấu hình không
2. Khởi động lại backend server
3. Kiểm tra logs của server để xem lỗi chi tiết

### Lỗi khi CRUD

1. Kiểm tra kết nối database
2. Xem logs để kiểm tra lỗi validation
3. Đảm bảo dữ liệu đầu vào hợp lệ

### API không hoạt động

1. Kiểm tra backend server có đang chạy không
2. Kiểm tra URL trong `frontend/lib/config/api_config.dart`
3. Xem network tab trong browser developer tools

## Files đã tạo/sửa đổi

### Backend
- `backend/app/core/config.py` - Thêm admin credentials
- `backend/app/api/admin.py` - Admin endpoints (MỚI)
- `backend/app/schemas/admin.py` - Admin schemas (MỚI)
- `backend/app/api/__init__.py` - Đăng ký admin router

### Frontend
- `frontend/lib/services/admin_service.dart` - Admin service (MỚI)
- `frontend/lib/screens/admin/admin_login_screen.dart` - Màn hình đăng nhập admin (MỚI)
- `frontend/lib/screens/admin/admin_dashboard_screen.dart` - Dashboard admin (MỚI)
- `frontend/lib/screens/admin/admin_users_screen.dart` - Quản lý users (MỚI)
- `frontend/lib/screens/admin/admin_units_screen.dart` - Quản lý units (MỚI)
- `frontend/lib/screens/admin/admin_categories_screen.dart` - Quản lý categories (MỚI)
- `frontend/lib/main.dart` - Thêm admin route
- `frontend/lib/screens/auth/login_screen.dart` - Thêm link Admin Panel

## Test API với Postman

### 1. Login

```http
POST http://localhost:8000/api/v1/admin/login
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

### 2. Get All Users

```http
GET http://localhost:8000/api/v1/admin/users?skip=0&limit=100
Authorization: Bearer {your_access_token}
```

### 3. Create User

```http
POST http://localhost:8000/api/v1/admin/users
Authorization: Bearer {your_access_token}
Content-Type: application/json

{
    "email": "newuser@example.com",
    "password": "password123",
    "name": "New User",
    "username": "newuser",
    "is_activated": true,
    "is_verified": false
}
```

## Liên hệ hỗ trợ

Nếu có vấn đề, vui lòng tạo issue trên GitHub repository hoặc liên hệ team phát triển.
