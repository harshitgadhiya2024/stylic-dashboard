# Stylic AI - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   iOS App    │  │ Android App  │  │   Web App    │          │
│  │ React Native │  │ React Native │  │  (Optional)  │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│         └──────────────────┴──────────────────┘                  │
│                            │                                      │
│                            │ HTTPS/REST API                       │
│                            │                                      │
└────────────────────────────┼──────────────────────────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────────┐
│                         API GATEWAY                               │
├────────────────────────────┼──────────────────────────────────────┤
│                            │                                       │
│                    ┌───────▼────────┐                            │
│                    │   FastAPI App  │                            │
│                    │   (Uvicorn)    │                            │
│                    └───────┬────────┘                            │
│                            │                                       │
│         ┌──────────────────┼──────────────────┐                  │
│         │                  │                  │                   │
│    ┌────▼─────┐     ┌─────▼──────┐    ┌─────▼──────┐           │
│    │   CORS   │     │  Logging   │    │   Auth     │           │
│    │Middleware│     │ Middleware │    │ Middleware │           │
│    └──────────┘     └────────────┘    └────────────┘           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────────┐
│                      APPLICATION LAYER                            │
├────────────────────────────┼──────────────────────────────────────┤
│                            │                                       │
│    ┌───────────────────────▼────────────────────────┐            │
│    │              API Endpoints (v1)                 │            │
│    ├─────────────────────────────────────────────────┤            │
│    │  /auth  │  /users  │  /photoshoots  │  /payments│           │
│    └────┬─────────┬──────────┬─────────────┬────────┘            │
│         │         │          │             │                      │
│    ┌────▼─────────▼──────────▼─────────────▼────────┐            │
│    │              Business Logic Layer               │            │
│    ├─────────────────────────────────────────────────┤            │
│    │  User      │  Email    │  Photoshoot │  Payment│            │
│    │  Service   │  Service  │  Service    │  Service│            │
│    └────┬─────────┬──────────┬─────────────┬────────┘            │
│         │         │          │             │                      │
└─────────┼─────────┼──────────┼─────────────┼──────────────────────┘
          │         │          │             │
┌─────────┼─────────┼──────────┼─────────────┼──────────────────────┐
│      DATA ACCESS LAYER                                            │
├─────────┼─────────┼──────────┼─────────────┼──────────────────────┤
│         │         │          │             │                       │
│    ┌────▼─────────▼──────────▼─────────────▼────────┐            │
│    │           MongoDB Service (Motor)               │            │
│    │         Async Database Operations               │            │
│    └────┬─────────┬──────────┬─────────────┬────────┘            │
│         │         │          │             │                      │
└─────────┼─────────┼──────────┼─────────────┼──────────────────────┘
          │         │          │             │
┌─────────┼─────────┼──────────┼─────────────┼──────────────────────┐
│      DATABASE & EXTERNAL SERVICES                                 │
├─────────┼─────────┼──────────┼─────────────┼──────────────────────┤
│         │         │          │             │                       │
│    ┌────▼────┐ ┌──▼──────┐ ┌▼──────────┐ ┌▼──────────┐          │
│    │ MongoDB │ │  SMTP   │ │  Razorpay │ │  AI APIs  │          │
│    │Database │ │ Server  │ │  Gateway  │ │ (OpenAI)  │          │
│    └─────────┘ └─────────┘ └───────────┘ └───────────┘          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## 🔄 Request Flow

### 1. Authentication Flow

```
User → Register → FastAPI → Validate → Generate OTP → Send Email
                                                    ↓
User ← Tokens ← Create User ← Verify OTP ← Check Email
```

### 2. Photoshoot Creation Flow

```
User → Upload Images → FastAPI → Validate Credits → Save to DB
                                        ↓
                                  Queue Processing
                                        ↓
                                  AI Generation
                                        ↓
                                  Save Results
                                        ↓
User ← Notification ← Update Status ← Complete
```

### 3. Payment Flow

```
User → Select Plan → FastAPI → Create Order → Razorpay
                                        ↓
User ← Redirect ← Order Details ← Razorpay Response
                                        ↓
User → Complete Payment → Razorpay → Webhook → FastAPI
                                                    ↓
                                              Verify Payment
                                                    ↓
                                              Update Credits
                                                    ↓
User ← Confirmation ← Send Email ← Update Database
```

## 📦 Component Architecture

### Backend Components

```
FastAPI Application
├── Core
│   ├── Configuration (Pydantic Settings)
│   ├── Security (JWT, Hashing)
│   └── Logging (Structured JSON)
│
├── API Layer
│   ├── Endpoints (Route Handlers)
│   ├── Dependencies (Auth, Validation)
│   └── Middleware (CORS, Logging)
│
├── Business Logic
│   ├── User Service
│   ├── Email Service
│   ├── Photoshoot Service
│   ├── Payment Service
│   └── AI Service
│
├── Data Access
│   ├── MongoDB Service
│   └── File Storage Service
│
└── Models
    ├── Pydantic Schemas
    └── Database Models
```

### Frontend Components (Planned)

```
React Native Application
├── Navigation
│   ├── Auth Stack
│   ├── Main Stack
│   └── Modal Stack
│
├── Screens
│   ├── Authentication
│   ├── Dashboard
│   ├── Photoshoot
│   ├── Gallery
│   └── Profile
│
├── Components
│   ├── UI Components
│   ├── Form Components
│   └── Layout Components
│
├── Services
│   ├── API Client
│   ├── Auth Service
│   └── Storage Service
│
├── State Management
│   ├── Redux Store
│   ├── Slices
│   └── Selectors
│
└── Theme
    ├── Colors
    ├── Typography
    └── Spacing
```

## 🔐 Security Architecture

### Authentication & Authorization

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ 1. Login Request
       ▼
┌─────────────┐
│   FastAPI   │
└──────┬──────┘
       │ 2. Validate Credentials
       ▼
┌─────────────┐
│   MongoDB   │
└──────┬──────┘
       │ 3. User Found
       ▼
┌─────────────┐
│   FastAPI   │
└──────┬──────┘
       │ 4. Generate JWT
       ▼
┌─────────────┐
│   Client    │ 5. Store Token
└──────┬──────┘
       │ 6. Authenticated Request
       │    (Authorization: Bearer <token>)
       ▼
┌─────────────┐
│   FastAPI   │ 7. Verify Token
└──────┬──────┘
       │ 8. Extract User
       ▼
┌─────────────┐
│  Protected  │ 9. Process Request
│  Resource   │
└─────────────┘
```

### Security Layers

1. **Transport Security**: HTTPS/TLS
2. **Authentication**: JWT tokens
3. **Authorization**: Role-based access control
4. **Input Validation**: Pydantic schemas
5. **Password Security**: bcrypt hashing
6. **Rate Limiting**: Request throttling (planned)
7. **CORS**: Configured origins
8. **SQL Injection**: NoSQL with validation

## 💾 Data Architecture

### Database Collections

```
MongoDB (stylic)
├── company_data
│   ├── id (UUID)
│   ├── email
│   ├── password (hashed)
│   ├── first_name
│   ├── last_name
│   ├── company_name
│   ├── phone
│   ├── credit
│   ├── plan
│   ├── role
│   ├── is_active
│   ├── created_at
│   └── updated_at
│
├── login_mapping
│   ├── id (UUID)
│   ├── email
│   ├── password (hashed)
│   ├── role
│   ├── is_active
│   ├── created_at
│   └── updated_at
│
├── photoshoot_data
│   ├── id (User UUID)
│   ├── photoshoot_id (UUID)
│   ├── upload_garment_type
│   ├── age_group
│   ├── gender
│   ├── ethnicity
│   ├── height
│   ├── width
│   ├── fitting
│   ├── background_description
│   ├── selected_background
│   ├── pose_input_method
│   ├── selected_poses
│   ├── pose_descriptions
│   ├── all_images
│   ├── total_credit
│   ├── is_credit_debited
│   ├── is_completed
│   ├── status
│   ├── created_at
│   └── updated_at
│
└── order_data
    ├── id (User UUID)
    ├── order_id
    ├── payment_id
    ├── credit
    ├── amount
    ├── currency
    ├── status
    ├── created_at
    └── updated_at
```

## 🚀 Deployment Architecture

### Development Environment

```
Developer Machine
├── Backend (localhost:8000)
├── MongoDB (localhost:27017 or Atlas)
└── Frontend (localhost:19006)
```

### Production Environment (Planned)

```
┌─────────────────────────────────────┐
│         Load Balancer               │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼───┐
│Backend │      │Backend │
│Server 1│      │Server 2│
└───┬────┘      └────┬───┘
    │                │
    └────────┬───────┘
             │
    ┌────────▼────────┐
    │   MongoDB       │
    │   Cluster       │
    └─────────────────┘
```

## 📊 Scalability Considerations

### Horizontal Scaling
- Multiple FastAPI instances behind load balancer
- Stateless API design
- JWT tokens (no server-side sessions)

### Database Scaling
- MongoDB replica sets
- Read replicas for queries
- Sharding for large datasets

### Caching (Planned)
- Redis for session data
- CDN for static assets
- API response caching

### Background Processing
- Celery for async tasks
- Queue for photoshoot generation
- Scheduled jobs for cleanup

## 🔄 CI/CD Pipeline (Planned)

```
Git Push → GitHub Actions → Tests → Build → Deploy
                                      ↓
                                   Docker
                                      ↓
                              Container Registry
                                      ↓
                              Kubernetes/Cloud
```

---

**Last Updated**: 2025-10-09
**Version**: 1.0.0

