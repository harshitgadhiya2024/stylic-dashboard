# Stylic AI - Quick Start Guide

## 🚀 Quick Start

This guide will help you get the Stylic AI application up and running quickly.

## Prerequisites

- Python 3.9 or higher
- MongoDB 4.4 or higher (or MongoDB Atlas account)
- Node.js 16+ and npm/yarn (for frontend)
- Git

## Backend Setup (5 minutes)

### 1. Navigate to Backend Directory
```bash
cd application/backend
```

### 2. Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configuration
# Required variables:
# - MONGO_URL (your MongoDB connection string)
# - SECRET_KEY (generate a secure random string)
# - SMTP credentials (for email)
# - RAZORPAY credentials (for payments)
# - AI API keys (OpenAI, Google AI, or Anthropic)
```

### 5. Create Required Directories
```bash
mkdir -p logs uploads/photoshoots uploads/poses uploads/garments
```

### 6. Run the Application
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python app/main.py
```

### 7. Access API Documentation
Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Testing the API

### 1. Register a New User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "Test Company",
    "phone": "1234567890",
    "is_privacy_accepted": true
  }'
```

### 2. Verify OTP
Check your email for the OTP, then:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/verify-otp?email=test@example.com" \
  -H "Content-Type: application/json" \
  -d '{
    "otp": 123456
  }'
```

### 3. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

You'll receive an `access_token` in the response. Use this token for authenticated requests:

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Environment Variables Explained

### Required Variables

```env
# Application
APP_NAME=Stylic AI
APP_ENV=development
DEBUG=True

# Security - IMPORTANT: Change in production!
SECRET_KEY=your-secret-key-here-change-in-production

# Database - Use your MongoDB connection string
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=stylic

# Email Configuration
SMTP_SERVER=smtp.hostinger.com
SMTP_PORT=587
SMTP_USERNAME=info@stylic.ai
SMTP_PASSWORD=your-smtp-password
EMAIL_FROM=info@stylic.ai

# Razorpay (Get from https://dashboard.razorpay.com/)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# AI APIs (Optional - for photoshoot generation)
OPENAI_API_KEY=your-openai-api-key
GOOGLE_AI_API_KEY=your-google-ai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### Optional Variables

```env
# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

# CORS (Add your frontend URLs)
CORS_ORIGINS=http://localhost:3000,http://localhost:19006

# File Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Credits
DEFAULT_SIGNUP_CREDITS=5
```

## Common Issues & Solutions

### Issue: MongoDB Connection Failed
**Solution**: 
- Check your `MONGO_URL` in `.env`
- Ensure MongoDB is running
- Check network connectivity
- Verify credentials

### Issue: Email Not Sending
**Solution**:
- Verify SMTP credentials in `.env`
- Check SMTP server and port
- Ensure firewall allows SMTP connections
- Check email logs in `logs/app.log`

### Issue: Import Errors
**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port Already in Use
**Solution**:
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001

# Or kill the process using port 8000
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Development Tips

### 1. Auto-reload on Code Changes
The `--reload` flag enables auto-reload:
```bash
uvicorn app.main:app --reload
```

### 2. View Logs
```bash
# Real-time log viewing
tail -f logs/app.log

# View error logs
tail -f logs/error.log
```

### 3. Test API with Swagger UI
Navigate to http://localhost:8000/docs for interactive API testing

### 4. Database Inspection
Use MongoDB Compass or mongo shell to inspect your database:
```bash
mongo "your-mongodb-connection-string"
use stylic
db.company_data.find()
```

## Production Deployment

### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
```bash
# Build image
docker build -t stylic-backend .

# Run container
docker run -d -p 8000:8000 --env-file .env stylic-backend
```

### Environment Variables for Production
```env
APP_ENV=production
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
LOG_LEVEL=WARNING
```

## Next Steps

1. ✅ Backend is running
2. 📱 Set up React Native frontend (coming soon)
3. 🔗 Connect frontend to backend
4. 🧪 Test the complete flow
5. 🚀 Deploy to production

## Getting Help

- Check `application/backend/README.md` for detailed documentation
- View API documentation at http://localhost:8000/docs
- Check logs in `logs/` directory
- Review `PROJECT_SUMMARY.md` for project overview

## Useful Commands

```bash
# Start backend
cd application/backend
source venv/bin/activate
uvicorn app.main:app --reload

# Run tests (when implemented)
pytest

# Check code style
black app/
flake8 app/

# View logs
tail -f logs/app.log

# Database backup
mongodump --uri="your-mongodb-uri" --out=backup/
```

---

**Happy Coding! 🚀**

