# API Overview

## Introduction

The Di Cho Tien Loi API is built using FastAPI and provides a comprehensive RESTful interface for food management operations. All endpoints are accessible under the `/api/v1` prefix and follow REST conventions with proper HTTP status codes and JSON responses.

## Base URL and Versioning

**Base URL**: `https://your-domain.com/api/v1`

All API endpoints are versioned using URL path versioning. The current version is v1, and all endpoints are prefixed with `/api/v1`.

## Authentication

### Authentication Flow
The API uses JWT (JSON Web Token) based authentication with access and refresh token mechanism:

1. **Registration/Login**: Client receives access token (15 minutes) and refresh token (7 days)
2. **API Requests**: Include `Authorization: Bearer <access_token>` header
3. **Token Refresh**: Use refresh token to get new access token when expired
4. **Logout**: Invalidate both tokens

### Authentication Headers
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

## Response Format

### Success Responses
All successful responses follow a consistent structure:

```json
{
  "data": {
    // Response data here
  },
  "message": "Operation successful",
  "status": "success"
}
```

### Error Responses
Error responses include detailed information for debugging:

```json
{
  "detail": "Error description",
  "error_code": "VALIDATION_ERROR",
  "status": "error",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### HTTP Status Codes
- **200**: Success
- **201**: Created successfully
- **400**: Bad request (validation error)
- **401**: Unauthorized (invalid/expired token)
- **403**: Forbidden (insufficient permissions)
- **404**: Resource not found
- **422**: Unprocessable entity (validation error)
- **429**: Rate limit exceeded
- **500**: Internal server error

## API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password123",
  "name": "John Doe",
  "username": "johndoe"
}
```

**Response:**
```json
{
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "username": "johndoe",
      "is_verified": false,
      "created_at": "2024-01-15T10:30:00Z"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJ...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJ...",
    "token_type": "bearer"
  }
}
```

#### Login
```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJ..."
}
```

#### Logout
```http
POST /api/v1/auth/logout
```

### User Management Endpoints

#### Get Current User Profile
```http
GET /api/v1/users/me
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "username": "johndoe",
    "avatar_url": "https://storage.example.com/avatars/user1.jpg",
    "language": "en",
    "timezone": "UTC",
    "is_active": true,
    "is_verified": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Update User Profile
```http
PUT /api/v1/users/me
```

**Request Body:**
```json
{
  "name": "John Updated",
  "language": "vi",
  "timezone": "Asia/Ho_Chi_Minh"
}
```

#### Upload Avatar
```http
POST /api/v1/users/me/avatar
Content-Type: multipart/form-data
```

**Form Data:**
```
avatar: [image file]
```

### Group Management Endpoints

#### Create Group
```http
POST /api/v1/groups
```

**Request Body:**
```json
{
  "name": "My Family",
  "description": "Our family food management group"
}
```

#### Get User Groups
```http
GET /api/v1/groups
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "My Family",
      "description": "Our family food management group",
      "owner_id": 1,
      "created_at": "2024-01-15T10:30:00Z",
      "member_count": 4,
      "role": "owner"
    }
  ]
}
```

#### Get Group Members
```http
GET /api/v1/groups/{group_id}/members
```

#### Add Group Member
```http
POST /api/v1/groups/{group_id}/members
```

**Request Body:**
```json
{
  "email": "member@example.com",
  "role": "member"
}
```

#### Remove Group Member
```http
DELETE /api/v1/groups/{group_id}/members/{user_id}
```

### Category and Unit Management

#### Get Categories
```http
GET /api/v1/categories?group_id={group_id}
```

#### Create Category
```http
POST /api/v1/categories
```

**Request Body:**
```json
{
  "name": "Vegetables",
  "group_id": 1
}
```

#### Get Units
```http
GET /api/v1/units?group_id={group_id}
```

#### Create Unit
```http
POST /api/v1/units
```

**Request Body:**
```json
{
  "name": "kg",
  "group_id": 1
}
```

### Food Management Endpoints

#### Get Foods
```http
GET /api/v1/foods?group_id={group_id}&category_id={category_id}&search={keyword}
```

**Query Parameters:**
- `group_id` (required): Group identifier
- `category_id` (optional): Filter by category
- `search` (optional): Search by food name
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20)

**Response:**
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Tomato",
        "category": {
          "id": 1,
          "name": "Vegetables"
        },
        "unit": {
          "id": 1,
          "name": "kg"
        },
        "image_url": "https://storage.example.com/foods/tomato.jpg",
        "created_by": 1,
        "group_id": 1,
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "total": 25,
    "page": 1,
    "limit": 20,
    "has_next": true
  }
}
```

#### Create Food
```http
POST /api/v1/foods
Content-Type: multipart/form-data
```

**Form Data:**
```
name: Tomato
category_id: 1
unit_id: 1
group_id: 1
image: [image file] (optional)
```

#### Update Food
```http
PUT /api/v1/foods/{food_id}
```

#### Delete Food
```http
DELETE /api/v1/foods/{food_id}
```

### Fridge Management Endpoints

#### Get Fridge Items
```http
GET /api/v1/fridge?group_id={group_id}&expiring_soon={boolean}
```

**Query Parameters:**
- `group_id` (required): Group identifier
- `expiring_soon` (optional): Filter items expiring within 3 days
- `expired` (optional): Filter expired items
- `sort` (optional): Sort by 'name', 'expiry_date', 'created_at'

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "food": {
        "id": 1,
        "name": "Tomato",
        "category": {"id": 1, "name": "Vegetables"},
        "unit": {"id": 1, "name": "kg"},
        "image_url": "https://storage.example.com/foods/tomato.jpg"
      },
      "quantity": 2.5,
      "note": "Fresh from market",
      "use_within_date": "2024-01-20T00:00:00Z",
      "days_until_expiry": 5,
      "is_expired": false,
      "created_by": {
        "id": 1,
        "name": "John Doe"
      },
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Add Item to Fridge
```http
POST /api/v1/fridge
```

**Request Body:**
```json
{
  "food_id": 1,
  "group_id": 1,
  "quantity": 2.5,
  "note": "Fresh from market",
  "use_within_date": "2024-01-20"
}
```

#### Update Fridge Item
```http
PUT /api/v1/fridge/{item_id}
```

#### Delete Fridge Item
```http
DELETE /api/v1/fridge/{item_id}
```

### Shopping List Endpoints

#### Get Shopping Lists
```http
GET /api/v1/shopping-lists?group_id={group_id}&archived={boolean}
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Weekly Shopping",
      "group_id": 1,
      "assigned_to": {
        "id": 2,
        "name": "Jane Doe"
      },
      "date": "2024-01-20T00:00:00Z",
      "note": "Don't forget the milk!",
      "is_archived": false,
      "task_count": 5,
      "completed_task_count": 2,
      "created_by": {
        "id": 1,
        "name": "John Doe"
      },
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Shopping List
```http
POST /api/v1/shopping-lists
```

**Request Body:**
```json
{
  "name": "Weekly Shopping",
  "group_id": 1,
  "assign_to_user_id": 2,
  "date": "2024-01-20",
  "note": "Don't forget the milk!"
}
```

#### Get Shopping List Tasks
```http
GET /api/v1/shopping-lists/{list_id}/tasks
```

#### Add Tasks to Shopping List
```http
POST /api/v1/shopping-lists/{list_id}/tasks
```

**Request Body:**
```json
{
  "tasks": [
    {
      "food_id": 1,
      "quantity": 2.5
    },
    {
      "food_id": 2,
      "quantity": 1.0
    }
  ]
}
```

#### Update Task Status
```http
PUT /api/v1/shopping-tasks/{task_id}
```

**Request Body:**
```json
{
  "is_done": true,
  "quantity": 3.0
}
```

### Meal Planning Endpoints

#### Get Meal Plans
```http
GET /api/v1/meal-plans?group_id={group_id}&date={YYYY-MM-DD}&meal_type={breakfast|lunch|dinner}
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Pasta with Tomato Sauce",
      "group_id": 1,
      "plan_date": "2024-01-20T00:00:00Z",
      "meal_type": "dinner",
      "foods": [
        {
          "id": 1,
          "name": "Pasta",
          "quantity": 0.5
        },
        {
          "id": 2,
          "name": "Tomato Sauce",
          "quantity": 1.0
        }
      ],
      "recipe": {
        "id": 1,
        "name": "Simple Pasta Recipe",
        "description": "Quick and easy pasta"
      },
      "created_by": {
        "id": 1,
        "name": "John Doe"
      },
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Meal Plan
```http
POST /api/v1/meal-plans
```

**Request Body:**
```json
{
  "name": "Pasta with Tomato Sauce",
  "group_id": 1,
  "plan_date": "2024-01-20",
  "meal_type": "dinner",
  "food_ids": [1, 2]
}
```

### Recipe Management Endpoints

#### Get Recipes
```http
GET /api/v1/recipes?group_id={group_id}&food_id={food_id}
```

#### Create Recipe
```http
POST /api/v1/recipes
```

**Request Body:**
```json
{
  "name": "Simple Pasta Recipe",
  "description": "Quick and easy pasta for busy weeknights",
  "html_content": "<h2>Ingredients</h2><ul><li>200g pasta</li><li>1 jar tomato sauce</li></ul><h2>Instructions</h2><ol><li>Boil pasta</li><li>Heat sauce</li><li>Combine and serve</li></ol>",
  "group_id": 1,
  "food_id": 1
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Authentication endpoints**: 5 requests per minute per IP
- **General endpoints**: 100 requests per minute per user
- **File upload endpoints**: 10 requests per minute per user

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248000
```

## Error Handling

### Validation Errors
When request validation fails, the API returns detailed field-level errors:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_FAILED`: Invalid credentials
- `TOKEN_EXPIRED`: Access token expired
- `INSUFFICIENT_PERMISSIONS`: User lacks required permissions
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `DUPLICATE_RESOURCE`: Resource already exists
- `RATE_LIMIT_EXCEEDED`: Too many requests

## Interactive Documentation

### Swagger UI
Available at `/docs` - provides interactive API documentation where you can:
- Browse all endpoints and their parameters
- Test API calls directly from the browser
- View request/response schemas
- Authenticate and make authorized requests

### ReDoc
Available at `/redoc` - provides clean, readable API documentation with:
- Detailed endpoint descriptions
- Request/response examples
- Schema definitions
- Authentication requirements

## SDK and Client Libraries

While the API can be consumed directly via HTTP requests, consider creating client libraries for different platforms:

- **React Native**: Axios-based HTTP client with authentication handling
- **Flutter**: Dio-based HTTP client with automatic token refresh
- **Python**: Official Python SDK for server-to-server integrations
- **JavaScript/TypeScript**: NPM package for web applications

## Webhook Support (Future)

The API is designed to support webhooks for real-time notifications:
- Food expiry alerts
- Shopping list assignments
- Group member additions
- Meal plan updates

Webhook endpoints will follow the pattern `/api/v1/webhooks/{event_type}` and include signature verification for security.