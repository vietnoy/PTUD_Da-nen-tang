# System Architecture

## Overview

The Di Cho Tien Loi platform is designed as a modern, scalable food management system using a microservices-oriented architecture. The system enables families and groups to efficiently manage their food inventory, plan meals, create shopping lists, and track food expiration dates.

## Technology Stack

### Backend Services
- **FastAPI**: Modern, fast web framework for building APIs with Python 3.11+
  - Automatic API documentation generation
  - Built-in data validation with Pydantic
  - Async/await support for high performance
  - Type hints for better code quality

- **PostgreSQL 15**: Primary relational database
  - ACID compliance for data integrity
  - Advanced indexing capabilities
  - JSON support for flexible data storage
  - Connection pooling for performance

- **Redis 7**: In-memory data structure store
  - Session storage and caching
  - Rate limiting implementation
  - Message broker for Celery tasks
  - Real-time data caching

- **Celery**: Distributed task queue system
  - Background job processing
  - Scheduled task execution (cron-like)
  - Retry mechanisms for failed tasks
  - Monitoring and logging capabilities

### Storage Solutions
- **MinIO**: S3-compatible object storage
  - Image and file uploads
  - Scalable storage solution
  - Compatible with AWS S3 APIs
  - Local development support

### Frontend Applications
- **React Native**: Cross-platform mobile application
  - Single codebase for iOS and Android
  - Native performance and user experience
  - Hot reload for faster development
  - Rich ecosystem of libraries

## System Architecture Layers

### 1. Presentation Layer
The presentation layer consists of mobile applications that interact with users:

**Mobile Applications (React Native/Flutter)**
- User interface for all food management features
- Real-time notifications for expiring items
- Offline capability for basic operations
- Camera integration for barcode scanning
- Push notification support

### 2. API Gateway Layer
**FastAPI Application Server**
- RESTful API endpoints following OpenAPI 3.0 specification
- JWT-based authentication and authorization
- Request/response validation using Pydantic models
- CORS configuration for cross-origin requests
- Rate limiting to prevent abuse
- Structured logging for monitoring

### 3. Business Logic Layer
**Service Layer Architecture**
```
app/
├── api/           # HTTP route handlers
├── services/      # Business logic implementation
├── repositories/  # Data access layer
├── schemas/       # Request/response models
├── models/        # Database entity definitions
├── core/          # Configuration and utilities
├── workers/       # Background task handlers
└── utils/         # Helper functions
```

**Key Components:**
- **Authentication Service**: User registration, login, JWT token management
- **Group Management Service**: Multi-user group operations and permissions
- **Food Inventory Service**: CRUD operations for food items and categories
- **Fridge Management Service**: Track food items with expiration dates
- **Shopping List Service**: Create and manage shopping tasks
- **Meal Planning Service**: Plan meals and generate shopping lists
- **Recipe Service**: Store and retrieve cooking recipes
- **Notification Service**: Send expiry alerts and task assignments

### 4. Data Access Layer
**Repository Pattern Implementation**
- Abstract data access operations
- Database query optimization
- Transaction management
- Connection pooling
- Migration support through Alembic

### 5. Data Storage Layer
**PostgreSQL Database Schema**
```
Users and Groups:
- users (authentication, profiles)
- groups (family/household units)
- group_members (user-group relationships)

Food Management:
- categories (food classification)
- units (measurement units)
- foods (food item definitions)
- fridge_items (inventory tracking)

Planning and Tasks:
- shopping_lists (shopping plans)
- shopping_tasks (individual items to buy)
- meal_plans (meal scheduling)
- meal_plan_items (foods in meals)
- recipes (cooking instructions)

Auditing:
- audit_logs (system activity tracking)
```

## Communication Patterns

### Synchronous Communication
- **Client to API**: HTTPS REST calls with JSON payloads
- **API to Database**: SQLAlchemy ORM queries
- **API to Redis**: Direct Redis protocol for caching

### Asynchronous Communication
- **Background Tasks**: Celery workers process long-running operations
- **Scheduled Jobs**: Celery beat scheduler for periodic tasks
- **Notifications**: Push notifications via Firebase Cloud Messaging

## Security Architecture

### Authentication and Authorization
- **JWT Tokens**: Stateless authentication with access and refresh tokens
- **Role-Based Access**: Group owners, admins, and members with different permissions
- **Password Security**: Bcrypt hashing for password storage
- **Token Rotation**: Automatic refresh token rotation for security

### Data Protection
- **Input Validation**: Pydantic models validate all incoming data
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **CORS Configuration**: Controlled cross-origin resource sharing
- **Rate Limiting**: Redis-based request rate limiting
- **HTTPS Encryption**: TLS encryption for all client communication

## Scalability Considerations

### Horizontal Scaling
- **API Servers**: Stateless FastAPI instances behind load balancer
- **Celery Workers**: Multiple worker processes for parallel task execution
- **Database Read Replicas**: Read-only database replicas for query scaling
- **Redis Clustering**: Redis cluster for high availability caching

### Performance Optimization
- **Database Indexing**: Strategic indexes on frequently queried columns
- **Query Optimization**: N+1 query prevention with eager loading
- **Caching Strategy**: Redis caching for frequently accessed data
- **Connection Pooling**: Database connection pooling for efficiency
- **Async Operations**: Non-blocking I/O operations where possible

## Deployment Architecture

### Development Environment
```
Docker Compose Services:
- backend: FastAPI application server
- worker: Celery worker processes
- scheduler: Celery beat scheduler
- db: PostgreSQL database
- redis: Redis cache and message broker
- minio: Object storage server
```

### Production Environment
- **Container Orchestration**: Kubernetes or Docker Swarm
- **Load Balancing**: Nginx or cloud load balancer
- **Database**: Managed PostgreSQL service
- **Object Storage**: AWS S3 or compatible service
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Logging**: Centralized logging with ELK stack

## Monitoring and Observability

### Health Checks
- **Liveness Probe**: `/healthz` endpoint for basic service health
- **Readiness Probe**: `/readyz` endpoint for dependency health
- **Detailed Status**: `/settings` endpoint for configuration verification

### Logging Strategy
- **Structured Logging**: JSON format for machine parsing
- **Request Tracing**: Unique request IDs for tracking
- **Error Tracking**: Comprehensive error logging with stack traces
- **Performance Metrics**: Response time and throughput monitoring

### Metrics Collection
- **Application Metrics**: Custom business metrics
- **System Metrics**: CPU, memory, disk usage
- **Database Metrics**: Query performance and connection counts
- **External Service Metrics**: Third-party API response times

## Data Flow Examples

### Adding Food to Fridge
1. Mobile app sends POST request to `/api/fridge` with food details
2. API validates request data using Pydantic schemas
3. Authentication middleware verifies JWT token
4. Authorization checks user's group membership
5. Service layer processes business logic
6. Repository saves data to PostgreSQL
7. Background task schedules expiry reminder
8. API returns success response to mobile app

### Expiry Notification Flow
1. Celery beat scheduler triggers daily expiry check
2. Worker queries database for items expiring in 3 days
3. For each expiring item, worker creates notification task
4. Notification service sends push notification via FCM
5. Mobile app receives and displays notification
6. User interaction tracked in audit logs

This architecture provides a solid foundation for a scalable, maintainable food management platform that can grow with user needs while maintaining performance and security standards.