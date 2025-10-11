# Stylic AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you quickly set up and run both the backend and frontend of Stylic AI.

---

## 📋 Prerequisites

### Backend Requirements
- Python 3.9+
- MongoDB (local or cloud)
- pip (Python package manager)

### Frontend Requirements
- Node.js 16+
- npm or yarn
- React Native development environment (for mobile)
- Xcode (for iOS, macOS only)
- Android Studio (for Android)

---

## 🔧 Backend Setup (FastAPI)

### 1. Navigate to Backend Directory
```bash
cd application/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

**Required Environment Variables:**
```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017/stylic_ai

# JWT
SECRET_KEY=your-secret-key-here
REFRESH_SECRET_KEY=your-refresh-secret-key-here

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Razorpay
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# AI Services
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_ai_key
OPENAI_API_KEY=your_openai_key
```

### 5. Run Backend Server
```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📱 Frontend Setup (React Native)

### 1. Navigate to Frontend Directory
```bash
cd application/frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Install iOS Dependencies (macOS only)
```bash
cd ios
pod install
cd ..
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env
nano .env
```

**Required Environment Variables:**
```env
API_BASE_URL=http://localhost:8000/api/v1
RAZORPAY_KEY_ID=your_razorpay_key_id
```

### 5. Run Frontend

#### iOS (macOS only)
```bash
npm run ios
# or
npx react-native run-ios
```

#### Android
```bash
npm run android
# or
npx react-native run-android
```

#### Start Metro Bundler (if not started automatically)
```bash
npm start
# or
npx react-native start
```

---

## 🧪 Testing

### Backend Tests
```bash
cd application/backend
pytest
# or with coverage
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd application/frontend
npm test
# or
yarn test
```

---

## 📊 Project Structure Overview

```
application/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints (29 endpoints)
│   │   ├── core/           # Configuration & security
│   │   ├── services/       # Business logic
│   │   ├── schemas/        # Pydantic models
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
│
└── frontend/               # React Native Frontend
    ├── src/
    │   ├── screens/        # App screens
    │   ├── components/     # Reusable components
    │   ├── navigation/     # Navigation setup
    │   ├── store/          # Redux store
    │   ├── services/       # API services
    │   ├── theme/          # Design system
    │   └── App.tsx         # Root component
    ├── ios/                # iOS native code
    ├── android/            # Android native code
    └── package.json        # Node dependencies
```

---

## 🔑 Key Features Implemented

### Backend (29 API Endpoints)
✅ Authentication (8 endpoints)
✅ User Management (5 endpoints)
✅ Payment Integration (6 endpoints)
✅ Photoshoot Management (7 endpoints)
✅ Credit Management (3 endpoints)

### Frontend
✅ Complete authentication flow
✅ Dashboard with statistics
✅ Photoshoot creation
✅ Gallery view
✅ Profile management
✅ Redux state management
✅ API integration with auto token refresh

---

## 🐛 Troubleshooting

### Backend Issues

**MongoDB Connection Error:**
```bash
# Check if MongoDB is running
mongosh

# Or start MongoDB service
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

**Port Already in Use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Metro Bundler Cache:**
```bash
npm start -- --reset-cache
```

**iOS Build Fails:**
```bash
cd ios
pod deintegrate
pod install
cd ..
```

**Android Build Fails:**
```bash
cd android
./gradlew clean
cd ..
```

---

## 📚 API Endpoints Quick Reference

### Authentication
- POST `/api/v1/auth/register` - Register user
- POST `/api/v1/auth/login` - Login user
- POST `/api/v1/auth/verify-otp` - Verify OTP
- POST `/api/v1/auth/refresh` - Refresh token

### Users
- GET `/api/v1/users/me` - Get profile
- PUT `/api/v1/users/me` - Update profile
- GET `/api/v1/users/me/credits` - Get credits

### Payments
- GET `/api/v1/payments/packages` - Get credit packages
- POST `/api/v1/payments/create-order` - Create order
- POST `/api/v1/payments/verify` - Verify payment

### Photoshoots
- POST `/api/v1/photoshoots` - Create photoshoot
- GET `/api/v1/photoshoots` - List photoshoots
- GET `/api/v1/photoshoots/{id}` - Get photoshoot details

### Credits
- GET `/api/v1/credits/balance` - Get balance
- GET `/api/v1/credits/history` - Get history

---

## 🔐 Default Test Credentials

**Note:** Create a new account through the registration flow.

---

## 📖 Additional Documentation

- **Backend README**: `application/backend/README.md`
- **Frontend README**: `application/frontend/README.md`
- **Frontend Setup Guide**: `application/frontend/SETUP.md`
- **Implementation Summary**: `application/IMPLEMENTATION_SUMMARY.md`

---

## 🆘 Need Help?

1. Check the detailed README files in each directory
2. Review the API documentation at http://localhost:8000/docs
3. Check the troubleshooting section above
4. Review the code comments and docstrings

---

## 🎯 Next Steps

1. ✅ Backend is fully functional
2. ✅ Frontend foundation is complete
3. ⏳ Implement remaining frontend features:
   - Complete photoshoot creation flow
   - Add payment integration (Razorpay)
   - Implement image upload and handling
   - Add animations and transitions
   - Complete all screen implementations

---

**Happy Coding! 🚀**

Last Updated: 2025-10-09
Version: 1.0.0

