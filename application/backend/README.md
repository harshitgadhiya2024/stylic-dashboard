# Stylic AI - FastAPI Backend

Production-level FastAPI backend for Stylic AI cross-platform application.

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/          # API route handlers
│   │       │   ├── auth.py         # Authentication endpoints
│   │       │   ├── users.py        # User management endpoints
│   │       │   ├── photoshoots.py  # Photoshoot endpoints
│   │       │   ├── payments.py     # Payment endpoints
│   │       │   └── credits.py      # Credit management endpoints
│   │       └── dependencies/       # Route dependencies
│   │           └── auth.py         # Authentication dependencies
│   ├── core/
│   │   ├── config.py              # Application configuration
│   │   ├── security.py            # Security utilities (JWT, hashing)
│   │   └── logging.py             # Logging configuration
│   ├── db/
│   │   ├── mongodb.py             # MongoDB connection manager
│   │   └── __init__.py
│   ├── models/                    # Database models (if needed)
│   ├── schemas/                   # Pydantic schemas
│   │   ├── user.py               # User schemas
│   │   ├── photoshoot.py         # Photoshoot schemas
│   │   ├── payment.py            # Payment schemas
│   │   └── __init__.py
│   ├── services/                  # Business logic services
│   │   ├── email_service.py      # Email sending service
│   │   ├── mongo_service.py      # MongoDB operations
│   │   ├── user_service.py       # User management service
│   │   ├── photoshoot_service.py # Photoshoot service
│   │   ├── payment_service.py    # Payment service
│   │   └── ai_service.py         # AI generation service
│   ├── utils/                     # Utility functions
│   │   ├── file_utils.py         # File handling utilities
│   │   └── validators.py         # Custom validators
│   └── main.py                    # FastAPI application entry point
├── tests/                         # Test files
│   ├── test_auth.py
│   ├── test_photoshoots.py
│   └── test_payments.py
├── logs/                          # Application logs
├── uploads/                       # Uploaded files
│   ├── photoshoots/
│   ├── poses/
│   └── garments/
├── .env                          # Environment variables
├── .env.example                  # Example environment variables
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
└── README.md                     # This file
```

## 🚀 Features

- **FastAPI Framework**: High-performance async API framework
- **JWT Authentication**: Secure token-based authentication
- **MongoDB**: Async MongoDB operations with Motor
- **Email Service**: Async email sending with HTML templates
- **Payment Integration**: Razorpay payment gateway integration
- **AI Integration**: OpenAI, Google AI, and Anthropic API support
- **File Upload**: Secure file upload with validation
- **Logging**: Structured JSON logging with rotation
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **CORS**: Configured for React Native frontend
- **Security**: Password hashing, input validation, rate limiting
- **Error Handling**: Comprehensive error handling and logging

## 📋 Prerequisites

- Python 3.9+
- MongoDB 4.4+
- SMTP server for email
- Razorpay account
- OpenAI/Google AI/Anthropic API keys

## 🛠️ Installation

1. **Clone the repository**
```bash
cd application/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Create required directories**
```bash
mkdir -p logs uploads/photoshoots uploads/poses uploads/garments
```

## 🏃 Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn (Production)
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: POST `/api/v1/auth/register`
2. **Verify OTP**: POST `/api/v1/auth/verify-otp`
3. **Login**: POST `/api/v1/auth/login`
4. **Get Token**: Receive `access_token` and `refresh_token`
5. **Use Token**: Include in header: `Authorization: Bearer <access_token>`

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/verify-otp` - Verify OTP
- `POST /api/v1/auth/resend-otp` - Resend OTP
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/forgot-password` - Request password reset
- `POST /api/v1/auth/reset-password` - Reset password
- `POST /api/v1/auth/change-password` - Change password

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users/me/credits` - Get credit balance

### Photoshoots
- `POST /api/v1/photoshoots` - Create photoshoot
- `GET /api/v1/photoshoots` - List photoshoots
- `GET /api/v1/photoshoots/{id}` - Get photoshoot details
- `GET /api/v1/photoshoots/filters` - Get filter options
- `GET /api/v1/photoshoots/{id}/download` - Download single image
- `GET /api/v1/photoshoots/{id}/download-all` - Download all images

### Payments
- `POST /api/v1/payments/create-order` - Create Razorpay order
- `POST /api/v1/payments/verify` - Verify payment
- `GET /api/v1/payments/validate-coupon` - Validate coupon code
- `GET /api/v1/payments/orders` - Get order history

### Credits
- `GET /api/v1/credits/history` - Get credit history
- `GET /api/v1/credits/balance` - Get credit balance

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 📝 Environment Variables

See `.env.example` for all required environment variables.

Key variables:
- `MONGO_URL`: MongoDB connection string
- `SECRET_KEY`: JWT secret key
- `RAZORPAY_KEY_ID`: Razorpay key ID
- `RAZORPAY_KEY_SECRET`: Razorpay key secret
- `SMTP_SERVER`: SMTP server address
- `OPENAI_API_KEY`: OpenAI API key

## 🐳 Docker Deployment

```bash
# Build image
docker build -t stylic-backend .

# Run container
docker run -d -p 8000:8000 --env-file .env stylic-backend
```

## 📊 Monitoring & Logging

- Logs are stored in `logs/` directory
- JSON format for easy parsing
- Automatic log rotation (10MB per file, 5 backups)
- Separate error log file

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Input validation with Pydantic
- CORS configuration
- Rate limiting
- Secure file upload validation
- SQL injection prevention (NoSQL)
- XSS protection

## 🤝 Contributing

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update documentation
4. Use type hints
5. Add docstrings to functions

## 📄 License

Copyright © 2025 Stylic AI. All rights reserved.

