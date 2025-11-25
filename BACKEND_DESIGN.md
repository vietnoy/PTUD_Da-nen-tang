# THIẾT KẾ BACKEND

## 1. Thiết kế cơ sở dữ liệu cho Backend

### 1.1 Mô hình hóa dữ liệu cho phía Backend

Hệ thống quản lý thực phẩm "Di Chợ Tiện Lợi" được thiết kế với mô hình cơ sở dữ liệu quan hệ gồm 9 bảng chính:

#### Sơ đồ thực thể liên kết (ER Diagram)

Sơ đồ ER được thể hiện trong file `database_schema.puml` bao gồm:

- **users**: Quản lý thông tin người dùng, xác thực và hồ sơ
- **groups**: Nhóm cho phép người dùng chia sẻ kho thực phẩm và danh sách mua sắm  
- **group_members**: Quản lý thành viên trong nhóm và vai trò của họ
- **categories**: Phân loại thực phẩm
- **units**: Đơn vị đo lường (trọng lượng, thể tích, số lượng)
- **foods**: Thông tin thực phẩm với hướng dẫn bảo quản
- **fridge_items**: Kho thực phẩm hiện tại của nhóm
- **shopping_lists**: Danh sách mua sắm được giao cho thành viên nhóm
- **shopping_tasks**: Các nhiệm vụ cụ thể trong danh sách mua sắm

### 1.2 Lược đồ cơ sở dữ liệu mức logic (Mô hình quan hệ)

Hệ thống sử dụng PostgreSQL với các mối quan hệ sau:

**Quan hệ một-nhiều:**
- User (1) -> Groups (n) - thông qua owner_id
- User (1) -> GroupMembers (n) - thông qua user_id  
- Group (1) -> GroupMembers (n) - thông qua group_id
- Category (1) -> Foods (n) - thông qua category_id
- Unit (1) -> Foods (n) - thông qua unit_id
- Food (1) -> FridgeItems (n) - thông qua food_id
- ShoppingList (1) -> ShoppingTasks (n) - thông qua list_id

**Quan hệ tự tham chiếu:**
- Unit (1) -> Unit (n) - thông qua base_unit_id (đơn vị gốc)

### 1.3 Đặc tả chi tiết các bảng dữ liệu

#### Bảng `users`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID người dùng |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email đăng nhập |
| password_hash | VARCHAR(255) | NOT NULL | Mật khẩu đã mã hóa |
| name | VARCHAR(100) | NOT NULL | Tên hiển thị |
| username | VARCHAR(50) | UNIQUE | Tên đăng nhập |
| type | VARCHAR(20) | | Loại tài khoản |
| language | VARCHAR(5) | DEFAULT 'en' | Ngôn ngữ |
| gender | VARCHAR(10) | | Giới tính |
| country_code | VARCHAR(10) | | Mã quốc gia |
| timezone | INTEGER | DEFAULT 0 | Múi giờ |
| birth_date | DATE | | Ngày sinh |
| photo_url | VARCHAR(500) | | URL ảnh đại diện |
| is_activated | BOOLEAN | DEFAULT true | Trạng thái kích hoạt |
| is_verified | BOOLEAN | DEFAULT false | Trạng thái xác minh |
| device_id | VARCHAR(255) | | ID thiết bị |
| belongs_to_group_admin_id | INTEGER | DEFAULT 0 | ID admin nhóm |
| created_at | TIMESTAMP | | Thời gian tạo |
| updated_at | TIMESTAMP | | Thời gian cập nhật |

#### Bảng `groups`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID nhóm |
| name | VARCHAR(100) | NOT NULL | Tên nhóm |
| description | TEXT | | Mô tả nhóm |
| owner_id | INTEGER | FK -> users.id | ID chủ nhóm |
| invite_code | VARCHAR(20) | UNIQUE | Mã mời vào nhóm |
| is_active | BOOLEAN | DEFAULT true | Trạng thái hoạt động |
| created_at | TIMESTAMP | | Thời gian tạo |
| updated_at | TIMESTAMP | | Thời gian cập nhật |

#### Bảng `group_members`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID thành viên nhóm |
| user_id | INTEGER | FK -> users.id | ID người dùng |
| group_id | INTEGER | FK -> groups.id | ID nhóm |
| role | VARCHAR(20) | DEFAULT 'member' | Vai trò (owner/admin/member) |
| is_active | BOOLEAN | DEFAULT true | Trạng thái hoạt động |
| joined_at | TIMESTAMP | | Thời gian tham gia |
| left_at | TIMESTAMP | | Thời gian rời nhóm |

#### Bảng `categories`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID danh mục |
| name | VARCHAR(50) | NOT NULL | Tên danh mục |
| description | TEXT | | Mô tả danh mục |
| created_at | TIMESTAMP | | Thời gian tạo |

#### Bảng `units`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID đơn vị |
| name | VARCHAR(20) | NOT NULL | Tên đơn vị |
| type | VARCHAR(20) | NOT NULL | Loại (weight/volume/count/length) |
| base_unit_id | INTEGER | FK -> units.id | ID đơn vị gốc |
| conversion_factor | DECIMAL(10,6) | | Hệ số chuyển đổi |
| created_at | TIMESTAMP | | Thời gian tạo |

#### Bảng `foods`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID thực phẩm |
| name | VARCHAR(100) | NOT NULL | Tên thực phẩm |
| description | TEXT | | Mô tả |
| category_id | INTEGER | FK -> categories.id | ID danh mục |
| unit_id | INTEGER | FK -> units.id | ID đơn vị |
| image_url | VARCHAR(500) | | URL hình ảnh |
| barcode | VARCHAR(50) | | Mã vạch |
| brand | VARCHAR(50) | | Thương hiệu |
| default_shelf_life_days | INTEGER | | Hạn sử dụng mặc định (ngày) |
| storage_instructions | TEXT | | Hướng dẫn bảo quản |
| group_id | INTEGER | FK -> groups.id | ID nhóm sở hữu |
| is_active | BOOLEAN | DEFAULT true | Trạng thái hoạt động |
| created_by | INTEGER | FK -> users.id | ID người tạo |
| created_at | TIMESTAMP | | Thời gian tạo |
| updated_at | TIMESTAMP | | Thời gian cập nhật |

#### Bảng `fridge_items`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID vật phẩm trong tủ lạnh |
| food_id | INTEGER | FK -> foods.id | ID thực phẩm |
| group_id | INTEGER | FK -> groups.id | ID nhóm |
| quantity | DECIMAL(8,3) | NOT NULL | Số lượng |
| unit_id | INTEGER | FK -> units.id | ID đơn vị |
| note | TEXT | | Ghi chú |
| purchase_date | DATE | | Ngày mua |
| use_within_date | DATE | NOT NULL | Hạn sử dụng |
| location | VARCHAR(50) | | Vị trí (fridge/pantry/freezer) |
| is_opened | BOOLEAN | DEFAULT false | Đã mở chưa |
| opened_at | TIMESTAMP | | Thời gian mở |
| cost | DECIMAL(8,2) | | Giá tiền |
| created_by | INTEGER | FK -> users.id | ID người tạo |
| created_at | TIMESTAMP | | Thời gian tạo |
| updated_at | TIMESTAMP | | Thời gian cập nhật |

#### Bảng `shopping_lists`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID danh sách mua sắm |
| name | VARCHAR(100) | NOT NULL | Tên danh sách |
| description | TEXT | | Mô tả |
| group_id | INTEGER | FK -> groups.id | ID nhóm |
| assign_to_user_id | INTEGER | FK -> users.id | ID người được giao |
| due_date | DATE | | Hạn hoàn thành |
| priority | VARCHAR(10) | DEFAULT 'medium' | Độ ưu tiên (low/medium/high) |
| status | VARCHAR(20) | DEFAULT 'active' | Trạng thái (draft/active/completed/cancelled) |
| budget | DECIMAL(10,2) | | Ngân sách |
| total_cost | DECIMAL(10,2) | DEFAULT 0 | Tổng chi phí |
| is_archived | BOOLEAN | DEFAULT false | Đã lưu trữ |
| created_by | INTEGER | FK -> users.id | ID người tạo |
| created_at | TIMESTAMP | | Thời gian tạo |
| updated_at | TIMESTAMP | | Thời gian cập nhật |

#### Bảng `shopping_tasks`
| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|--------|-------------|-----------|--------|
| id | INTEGER | PRIMARY KEY | ID nhiệm vụ mua sắm |
| list_id | INTEGER | FK -> shopping_lists.id (CASCADE) | ID danh sách |
| food_id | INTEGER | FK -> foods.id | ID thực phẩm |
| quantity | DECIMAL(8,3) | NOT NULL | Số lượng |
| unit_id | INTEGER | FK -> units.id | ID đơn vị |
| note | TEXT | | Ghi chú |
| estimated_cost | DECIMAL(8,2) | | Giá dự kiến |
| actual_cost | DECIMAL(8,2) | | Giá thực tế |
| priority | VARCHAR(10) | DEFAULT 'medium' | Độ ưu tiên |
| is_done | BOOLEAN | DEFAULT false | Đã hoàn thành |
| done_at | TIMESTAMP | | Thời gian hoàn thành |
| done_by | INTEGER | FK -> users.id | ID người hoàn thành |
| created_at | TIMESTAMP | | Thời gian tạo |
| updated_at | TIMESTAMP | | Thời gian cập nhật |

## 2. Thiết kế API Backend

### 2.1 Thông tin kết nối

**Đường dẫn cơ sở:** `https://localhost:8000/api/v1/` hoặc `https://dicho.example.com/api/v1/`

**Đường dẫn truy cập API:**
- Đăng ký: `POST https://localhost:8000/api/v1/auth/register`
- Đăng nhập: `POST https://localhost:8000/api/v1/auth/login`
- Quản lý nhóm: `GET/POST https://localhost:8000/api/v1/groups/`

**Content-Type:** `application/json`

### 2.2 Danh sách mã phản hồi (Response Codes)

Hệ thống sử dụng mã phản hồi thống nhất được định nghĩa trong `resultCode.py`:

| Mã | Thông báo | Mô tả |
|----|-----------|--------|
| 00098 | Thành công | Thao tác thành công chung |
| 00035 | Bạn đã đăng ký thành công | Đăng ký tài khoản thành công |
| 00047 | Bạn đã đăng nhập thành công | Đăng nhập thành công |
| 00050 | Đăng xuất thành công | Đăng xuất thành công |
| 00048 | Mã đã được gửi đến email của bạn thành công | Gửi mã xác minh thành công |
| 00058 | Địa chỉ email của bạn đã được xác minh thành công | Xác minh email thành công |
| 00095 | Tạo nhóm thành công | Tạo nhóm thành công |
| 00102 | Người dùng thêm vào nhóm thành công | Thêm thành viên vào nhóm |
| 00110 | Lấy các unit thành công | Lấy danh sách đơn vị |
| 00129 | Lấy các category thành công | Lấy danh sách danh mục |
| 00005 | Vui lòng cung cấp đầy đủ thông tin | Thiếu thông tin bắt buộc |
| 00006 | Truy cập bị từ chối. Không có token | Lỗi xác thực |
| 00007 | ID người dùng không hợp lệ | ID không hợp lệ |
| 00008 | Đã xảy ra lỗi máy chủ nội bộ | Lỗi server |
| 00093 | Không thể tạo nhóm, bạn đã thuộc về một nhóm rồi | Đã có nhóm |
| 00099 | Người này đã thuộc về một nhóm | Thành viên đã có nhóm |

### 2.3 Danh sách API

| STT | Danh sách API | Usecase / Mô tả |
|-----|---------------|-----------------|
| 1 | **Authentication APIs** | |
| | POST /auth/register | Đăng ký tài khoản mới |
| | POST /auth/login | Đăng nhập |
| | POST /auth/logout | Đăng xuất |
| | POST /auth/verify-email | Xác minh email |
| | POST /auth/send-verification-code | Gửi mã xác minh |
| | POST /auth/refresh-token | Làm mới token |
| 2 | **User Management APIs** | |
| | GET /users/profile | Lấy thông tin hồ sơ |
| | PUT /users/profile | Cập nhật thông tin hồ sơ |
| | DELETE /users/account | Xóa tài khoản |
| 3 | **Group Management APIs** | |
| | GET /groups/ | Lấy danh sách nhóm |
| | POST /groups/ | Tạo nhóm mới |
| | PUT /groups/{group_id} | Cập nhật thông tin nhóm |
| | DELETE /groups/{group_id} | Xóa nhóm |
| | POST /groups/join | Tham gia nhóm bằng mã mời |
| | POST /groups/{group_id}/members | Thêm thành viên vào nhóm |
| | DELETE /groups/{group_id}/members/{user_id} | Xóa thành viên khỏi nhóm |
| 4 | **Category Management APIs** | |
| | GET /categories/ | Lấy danh sách danh mục |
| | POST /categories/ | Tạo danh mục mới |
| | PUT /categories/{category_id} | Cập nhật danh mục |
| | DELETE /categories/{category_id} | Xóa danh mục |
| 5 | **Unit Management APIs** | |
| | GET /units/ | Lấy danh sách đơn vị |
| | POST /units/ | Tạo đơn vị mới |
| | PUT /units/{unit_id} | Cập nhật đơn vị |
| | DELETE /units/{unit_id} | Xóa đơn vị |

## 3. Đặc tả chi tiết API

### 3.1 API Đăng ký (Register)

**API URL:** `POST /api/v1/auth/register`

**Mô tả:** API thực hiện việc đăng ký tài khoản mới cho người dùng

**Request Header:**
- Method: POST  
- Content-Type: application/json

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "Nguyễn Văn A",
  "username": "nguyenvana",
  "language": "vn",
  "gender": "male",
  "country_code": "VN",
  "timezone": 7,
  "birth_date": "1990-01-01"
}
```

**Response:**
```json
{
  "resultMessage": {
    "en": "Registration successful",
    "vn": "Đăng ký thành công"
  },
  "resultCode": "00035",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Nguyễn Văn A",
    "username": "nguyenvana",
    "is_activated": true,
    "is_verified": false
  },
  "confirmToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Test Cases:**

1. **Đăng ký thành công với thông tin hợp lệ**
   - Input: Email chưa tồn tại, password hợp lệ (6-100 ký tự), name không trống
   - Expected: Code 00035, tạo user thành công, gửi email xác minh
   - Note: Email phải đúng định dạng, password tối thiểu 6 ký tự

2. **Email đã tồn tại**
   - Input: Email đã được đăng ký trước đó
   - Expected: Lỗi email đã tồn tại

3. **Email không đúng định dạng**
   - Input: Email không có @ hoặc domain không hợp lệ
   - Expected: Lỗi validation ngay phía client và server

4. **Password không đủ mạnh**
   - Input: Password < 6 ký tự hoặc quá đơn giản
   - Expected: Lỗi validation password

5. **Thiếu thông tin bắt buộc**
   - Input: Không có email, password hoặc name
   - Expected: Code 00005 - Thiếu thông tin bắt buộc

### 3.2 API Đăng nhập (Login)

**API URL:** `POST /api/v1/auth/login`

**Mô tả:** API xác thực người dùng và cấp access token

**Request Header:**
- Method: POST
- Content-Type: application/json  

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "resultMessage": {
    "en": "Login successful", 
    "vn": "Bạn đã đăng nhập thành công"
  },
  "resultCode": "00047",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Nguyễn Văn A"
  },
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Test Cases:**

1. **Đăng nhập thành công**
   - Input: Email và password chính xác
   - Expected: Code 00047, trả về access token và refresh token

2. **Sai email hoặc password**
   - Input: Email không tồn tại hoặc password sai
   - Expected: Lỗi xác thực, không trả về token

3. **Tài khoản chưa được kích hoạt**
   - Input: Email/password đúng nhưng is_activated = false  
   - Expected: Yêu cầu kích hoạt tài khoản

### 3.3 API Tạo nhóm (Create Group)

**API URL:** `POST /api/v1/groups/`

**Mô tả:** API tạo nhóm mới cho phép chia sẻ thực phẩm

**Request Header:**
- Method: POST
- Content-Type: application/json
- Authorization: Bearer {access_token}

**Request Body:**
```json
{
  "name": "Gia đình Nguyễn",
  "description": "Nhóm gia đình để quản lý thực phẩm chung"
}
```

**Response:**
```json
{
  "resultMessage": {
    "en": "Group created successfully",
    "vn": "Tạo nhóm thành công"  
  },
  "resultCode": "00095",
  "group": {
    "id": 1,
    "name": "Gia đình Nguyễn", 
    "description": "Nhóm gia đình để quản lý thực phẩm chung",
    "owner_id": 1,
    "invite_code": "ABC123",
    "is_active": true
  }
}
```

**Test Cases:**

1. **Tạo nhóm thành công**
   - Input: Tên nhóm hợp lệ, user chưa có nhóm
   - Expected: Code 00095, tạo nhóm và mã mời thành công

2. **User đã có nhóm**
   - Input: User đã là thành viên của nhóm khác
   - Expected: Code 00093 - Không thể tạo nhóm, đã thuộc về nhóm rồi

3. **Thiếu tên nhóm**
   - Input: Không cung cấp tên nhóm
   - Expected: Code 00005 - Thiếu thông tin bắt buộc

4. **Token không hợp lệ**
   - Input: Không có token hoặc token hết hạn
   - Expected: Code 00006 - Truy cập bị từ chối

### 3.4 API Lấy danh sách đơn vị (Get Units)

**API URL:** `GET /api/v1/units/`

**Mô tả:** API lấy danh sách các đơn vị đo lường

**Request Header:**
- Method: GET
- Authorization: Bearer {access_token}

**Response:**
```json
{
  "resultMessage": {
    "en": "Units fetched successfully",
    "vn": "Lấy các unit thành công"
  },
  "resultCode": "00110", 
  "units": [
    {
      "id": 1,
      "name": "kg",
      "type": "weight",
      "base_unit_id": null,
      "conversion_factor": null
    },
    {
      "id": 2, 
      "name": "gram",
      "type": "weight",
      "base_unit_id": 1,
      "conversion_factor": 0.001
    }
  ]
}
```

### 3.5 API Lấy danh sách danh mục (Get Categories)

**API URL:** `GET /api/v1/categories/`

**Mô tả:** API lấy danh sách các danh mục thực phẩm

**Request Header:**
- Method: GET
- Authorization: Bearer {access_token}

**Response:**
```json
{
  "resultMessage": {
    "en": "Categories fetched successfully", 
    "vn": "Lấy các category thành công"
  },
  "resultCode": "00129",
  "categories": [
    {
      "id": 1,
      "name": "Rau củ quả",
      "description": "Các loại rau, củ, quả tươi"
    },
    {
      "id": 2,
      "name": "Thịt cá",
      "description": "Thịt, cá, hải sản tươi sống"
    }
  ]
}
```

## 4. Cấu hình và Triển khai

### 4.1 Cấu hình môi trường

Hệ thống sử dụng các biến môi trường sau:

- `DATABASE_URL`: Kết nối PostgreSQL
- `REDIS_URL`: Kết nối Redis cho cache  
- `SECRET_KEY`: Khóa bí mật cho JWT
- `MINIO_ENDPOINT`: Endpoint cho lưu trữ file
- `ACCESS_TOKEN_EXPIRES_MINUTES`: Thời gian hết hạn access token
- `REFRESH_TOKEN_EXPIRES_MINUTES`: Thời gian hết hạn refresh token

### 4.2 Công nghệ sử dụng

- **Backend Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy  
- **Cache:** Redis
- **File Storage:** MinIO
- **Authentication:** JWT
- **Container:** Docker & Docker Compose

### 4.3 Cấu trúc thư mục

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Cấu hình core
│   ├── models/       # Database models  
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   ├── utils/        # Utilities
│   └── workers/      # Background tasks
├── alembic/          # Database migrations
├── tests/           # Test files
└── docker-compose.yml
```