# External Integrations

## Overview

The Di Cho Tien Loi platform integrates with several external services to provide comprehensive food management functionality. This document details each integration, its purpose, configuration requirements, and implementation considerations.

## Core Integrations

### 1. Object Storage - MinIO/Amazon S3

**Purpose:**
- Store food item images and photos
- User avatar and profile pictures
- Recipe images and cooking step illustrations
- System assets and media files
- Backup and archival storage

**Development Environment:**
MinIO provides S3-compatible object storage for local development:

```yaml
# docker-compose.yml
minio:
  image: minio/minio:latest
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  ports:
    - "9000:9000"  # API endpoint
    - "9001:9001"  # Console UI
  volumes:
    - minio_data:/data
```

**Production Options:**
- **Amazon S3**: Industry standard with global CDN integration
- **Google Cloud Storage**: Cost-effective with strong consistency
- **Azure Blob Storage**: Enterprise integration capabilities
- **DigitalOcean Spaces**: Developer-friendly pricing
- **Backblaze B2**: Lowest cost option

**Configuration:**
```bash
# MinIO/S3 Configuration
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=di-cho-media
MINIO_REGION=us-east-1

# Production S3 Configuration
AWS_S3_ENDPOINT=https://s3.amazonaws.com
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=di-cho-production
AWS_S3_REGION=us-west-2
```

**Implementation Details:**
- Automatic bucket creation on startup
- Image resizing and optimization (thumbnail, medium, large)
- Signed URLs for secure temporary access
- Multipart upload support for large files
- CDN integration for fast global delivery
- Automatic cleanup of orphaned files

**Usage Examples:**
```python
# Upload food image
async def upload_food_image(file: UploadFile) -> str:
    object_key = f"foods/{uuid4()}.jpg"
    await s3_client.upload_fileobj(file.file, bucket, object_key)
    return f"https://cdn.example.com/{object_key}"

# Generate presigned URL
def get_presigned_url(object_key: str, expires_in: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': object_key},
        ExpiresIn=expires_in
    )
```

### 2. Email Service Provider

**Purpose:**
- User account verification emails
- Password reset notifications
- Food expiry reminder emails
- Shopping list assignment notifications
- Weekly/monthly digest emails
- System maintenance notifications

**Development Environment:**
For local development, use console output or MailHog:

```yaml
# docker-compose.yml (optional)
mailhog:
  image: mailhog/mailhog:latest
  ports:
    - "1025:1025"  # SMTP
    - "8025:8025"  # Web UI
```

**Production Options:**

**SendGrid** (Recommended for high volume):
- Reliable delivery with 99% uptime SLA
- Advanced analytics and tracking
- Template management system
- Webhook support for delivery events
- Free tier: 100 emails/day

**Mailgun** (Developer-friendly):
- Simple REST API
- Powerful routing and filtering
- EU data residency options
- Free tier: 10,000 emails/month

**Amazon SES** (Cost-effective):
- Lowest cost per email sent
- Tight AWS ecosystem integration
- Reputation management tools
- Pay-as-you-go pricing

**Configuration:**
```bash
# Email Service Configuration
EMAIL_PROVIDER=sendgrid  # sendgrid, mailgun, ses, smtp
EMAIL_FROM_ADDRESS=noreply@dichotienloi.com
EMAIL_FROM_NAME=Di Cho Tien Loi

# SendGrid Configuration
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_TEMPLATE_ID_VERIFICATION=d-1234567890
SENDGRID_TEMPLATE_ID_PASSWORD_RESET=d-0987654321

# Mailgun Configuration
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=mail.dichotienloi.com
MAILGUN_BASE_URL=https://api.mailgun.net/v3

# Amazon SES Configuration
AWS_SES_REGION=us-east-1
AWS_SES_ACCESS_KEY_ID=your_ses_access_key
AWS_SES_SECRET_ACCESS_KEY=your_ses_secret_key

# SMTP Configuration (fallback)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_USE_TLS=true
```

**Email Templates:**
- **Account Verification**: Welcome message with verification link
- **Password Reset**: Secure password reset link with expiration
- **Expiry Alert**: Food items expiring in next 3 days
- **Shopping Assignment**: New shopping list assignment notification
- **Weekly Digest**: Summary of activities and upcoming expirations

**Implementation Features:**
- HTML and plain text versions
- Internationalization support (English, Vietnamese)
- Unsubscribe management
- Bounce and complaint handling
- Rate limiting and queue management
- A/B testing capabilities

### 3. Push Notification Service - Firebase Cloud Messaging (FCM)

**Purpose:**
- Real-time food expiry notifications
- Shopping list task assignments
- Group invitation alerts
- Meal planning reminders
- System announcements
- Background sync notifications

**Setup Requirements:**

1. **Firebase Project Setup:**
   - Create project at console.firebase.google.com
   - Enable Cloud Messaging API
   - Download service account JSON key
   - Configure mobile app with FCM SDK

2. **Service Account Configuration:**
   - Create service account with "Firebase Cloud Messaging Admin" role
   - Download JSON credentials file
   - Store securely (not in version control)

**Configuration:**
```bash
# FCM Configuration
FCM_PROJECT_ID=di-cho-tien-loi
FCM_CREDENTIALS_PATH=/app/secrets/firebase-credentials.json
FCM_ANDROID_PACKAGE=com.dichotienloi.app
FCM_IOS_BUNDLE_ID=com.dichotienloi.app

# Development/Testing
FCM_DEVELOPMENT_MODE=true
FCM_TEST_TOKENS=["token1", "token2"]  # For testing
```

**Message Types:**

**Data Messages** (background processing):
```json
{
  "data": {
    "type": "expiry_alert",
    "food_id": "123",
    "food_name": "Milk",
    "days_until_expiry": "2",
    "group_id": "456"
  }
}
```

**Notification Messages** (display directly):
```json
{
  "notification": {
    "title": "Food Expiring Soon!",
    "body": "Your milk expires in 2 days",
    "icon": "ic_expiry_warning",
    "sound": "default"
  }
}
```

**Topic-based Messaging:**
- Group-specific topics: `/topics/group_123`
- User-specific topics: `/topics/user_456`
- Global announcements: `/topics/all_users`

**Implementation Features:**
- Device token management and refresh
- Message scheduling and batching
- Delivery receipt tracking
- Platform-specific customization (iOS/Android)
- Rich notifications with images and actions
- Deep linking to specific app screens

### 4. Cache and Session Storage - Redis

**Purpose:**
- API response caching
- Session storage for authentication
- Rate limiting counters
- Real-time data synchronization
- Temporary data storage
- Queue management for background tasks

**Development Environment:**
```yaml
# docker-compose.yml
redis:
  image: redis:7-alpine
  command: redis-server --save 60 1 --loglevel warning
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
```

**Production Options:**
- **Amazon ElastiCache**: Managed Redis with automatic failover
- **Google Cloud Memorystore**: Fully managed with monitoring
- **Azure Cache for Redis**: Enterprise security features
- **Redis Cloud**: Official managed service
- **Self-managed**: Redis Sentinel or Cluster mode

**Configuration:**
```bash
# Redis Configuration
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=your_redis_password
REDIS_SSL=false
REDIS_TIMEOUT=30
REDIS_RETRY_ON_TIMEOUT=true

# Cache Settings
CACHE_DEFAULT_TTL=3600  # 1 hour
CACHE_FOODS_TTL=86400   # 24 hours
CACHE_USER_TTL=1800     # 30 minutes

# Rate Limiting
RATE_LIMIT_REDIS_DB=1
RATE_LIMIT_DEFAULT=100/hour
RATE_LIMIT_AUTH=5/minute
```

**Usage Patterns:**
- **API Caching**: Frequently accessed data (food lists, categories)
- **Session Management**: JWT token blacklist, user sessions
- **Rate Limiting**: Per-user request counters
- **Real-time Updates**: WebSocket connection state
- **Background Jobs**: Celery result storage

## Optional Integrations

### 5. Nutrition Data API

**Purpose:**
- Enrich food items with nutritional information
- Calculate meal nutritional values
- Provide dietary recommendations
- Support diet tracking features
- Generate health insights

**Provider Options:**

**Edamam Nutrition API** (Recommended):
- Comprehensive nutrition database
- Recipe analysis capabilities
- Diet and health label filtering
- Free tier: 1,000 requests/month
- Pricing: $0.006 per request

**Spoonacular API**:
- Food and recipe database
- Meal planning suggestions
- Ingredient substitution recommendations
- Free tier: 150 requests/day
- Pricing: $0.004 per point

**USDA FoodData Central**:
- Official US government nutrition data
- Free access with registration
- Limited to US food products
- No commercial restrictions

**Configuration:**
```bash
# Nutrition API Configuration
NUTRITION_PROVIDER=edamam  # edamam, spoonacular, usda

# Edamam Configuration
EDAMAM_APPLICATION_ID=your_app_id
EDAMAM_APPLICATION_KEY=your_app_key
EDAMAM_BASE_URL=https://api.edamam.com/api/food-database/v2

# Spoonacular Configuration
SPOONACULAR_API_KEY=your_api_key
SPOONACULAR_BASE_URL=https://api.spoonacular.com

# USDA Configuration
USDA_API_KEY=your_usda_key
USDA_BASE_URL=https://api.nal.usda.gov/fdc/v1
```

**Implementation Features:**
- Automatic nutrition data fetching for new foods
- Caching to minimize API calls
- Fallback to local database when API unavailable
- Batch processing for multiple foods
- Data quality validation and normalization

### 6. Barcode Scanning API

**Purpose:**
- Quick food identification via barcode scanning
- Automatic food information population
- Brand and product name recognition
- Nutritional information lookup
- Price comparison integration

**Provider Options:**

**Open Food Facts**:
- Open source food product database
- Free API access
- Community-driven data
- Covers international products
- No rate limits

**UPC Database**:
- Comprehensive product database
- Paid API with high accuracy
- Includes pricing information
- Good for commercial use
- Rate limits apply

**Barcode Lookup**:
- Simple product lookup
- Free tier available
- Good coverage of consumer products
- Easy integration
- Basic product information

**Configuration:**
```bash
# Barcode API Configuration
BARCODE_PROVIDER=openfoodfacts  # openfoodfacts, upcdb, barcodelookup

# Open Food Facts Configuration
OPENFOODFACTS_BASE_URL=https://world.openfoodfacts.org/api/v0
OPENFOODFACTS_USER_AGENT=DiChoTienLoi/1.0

# UPC Database Configuration
UPCDB_ACCESS_KEY=your_access_key
UPCDB_BASE_URL=https://api.upcdb.com

# Barcode Lookup Configuration
BARCODELOOKUP_API_KEY=your_api_key
BARCODELOOKUP_BASE_URL=https://api.barcodelookup.com/v3
```

### 7. Geolocation and Store Finder

**Purpose:**
- Find nearby grocery stores
- Store-specific pricing information
- Delivery service integration
- Location-based recommendations
- Regional food availability

**Provider Options:**

**Google Places API**:
- Comprehensive store database
- Real-time information (hours, ratings)
- Photo integration
- Detailed place information
- Pricing: $0.017 per request

**Foursquare Places API**:
- Rich venue data
- Category-specific search
- User-generated content
- Good international coverage
- Free tier: 1,000 requests/day

**Configuration:**
```bash
# Geolocation Configuration
PLACES_PROVIDER=google  # google, foursquare

# Google Places Configuration
GOOGLE_PLACES_API_KEY=your_google_key
GOOGLE_PLACES_BASE_URL=https://maps.googleapis.com/maps/api/place

# Foursquare Configuration
FOURSQUARE_CLIENT_ID=your_client_id
FOURSQUARE_CLIENT_SECRET=your_client_secret
FOURSQUARE_BASE_URL=https://api.foursquare.com/v3
```

## Integration Security

### API Key Management
- Store all API keys in environment variables
- Use different keys for development and production
- Implement key rotation procedures
- Monitor API usage and costs
- Set up usage alerts and limits

### Data Privacy
- Minimize data sent to external services
- Implement data anonymization where possible
- Regular privacy policy updates
- User consent management
- GDPR/CCPA compliance measures

### Error Handling
- Graceful degradation when services unavailable
- Retry logic with exponential backoff
- Circuit breaker pattern for unreliable services
- Fallback mechanisms for critical functionality
- Comprehensive logging and monitoring

## Monitoring and Observability

### Health Checks
Implement health checks for all external integrations:

```python
async def check_integration_health():
    results = {}

    # Check S3/MinIO connectivity
    try:
        await s3_client.head_bucket(Bucket=bucket_name)
        results['storage'] = 'healthy'
    except Exception as e:
        results['storage'] = f'unhealthy: {str(e)}'

    # Check Redis connectivity
    try:
        await redis_client.ping()
        results['cache'] = 'healthy'
    except Exception as e:
        results['cache'] = f'unhealthy: {str(e)}'

    # Check email service
    try:
        await email_client.test_connection()
        results['email'] = 'healthy'
    except Exception as e:
        results['email'] = f'unhealthy: {str(e)}'

    return results
```

### Metrics and Alerting
- API response times and error rates
- Storage usage and costs
- Email delivery rates
- Push notification success rates
- Cache hit rates and memory usage
- External service availability

## Cost Optimization

### Usage Monitoring
- Track API calls and associated costs
- Implement usage quotas and limits
- Regular cost analysis and optimization
- Budget alerts and controls
- Resource utilization monitoring

### Optimization Strategies
- Cache frequently accessed external data
- Batch API requests where possible
- Use appropriate service tiers
- Implement request deduplication
- Regular service provider evaluation

This comprehensive integration strategy ensures reliable, scalable, and cost-effective external service integration while maintaining security and performance standards.