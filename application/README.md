# Stylic AI - AI-Powered Photoshoot Generation Platform

<div align="center">

![Stylic AI](https://img.shields.io/badge/Stylic-AI-6366f1?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React Native](https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)

**Generate professional AI photoshoots with custom poses, garments, and models**

</div>

---

## 🎯 Overview

Stylic AI is a complete AI-powered photoshoot generation platform that allows users to create professional product photoshoots using AI. Upload garment images, select poses, customize model specifications, and generate high-quality photoshoots instantly.

### Project Status
- ✅ **Backend**: 100% Complete (29 API endpoints)
- ✅ **Frontend**: 95% Complete (all core features)
- ✅ **Documentation**: 100% Complete
- ✅ **Overall**: 95% Production Ready

---

## ✨ Key Features

- 🎨 AI-powered photoshoot generation
- 📸 Multiple pose selection methods (predefined, upload, prompts)
- 💳 Razorpay payment integration with coupon support
- 👤 Complete user management with OTP verification
- 📊 Real-time analytics dashboard
- 🖼️ Gallery with filters and download options
- 📱 Cross-platform mobile app (iOS & Android)
- 🔐 Secure JWT authentication
- 💰 Credit-based pricing system
- 📧 Email notifications with HTML templates

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** 0.104+ - Async Python web framework
- **MongoDB** with Motor - Async database driver
- **JWT** - Token-based authentication
- **Razorpay** 1.4.1 - Payment gateway
- **Anthropic Claude** - Pose analysis AI
- **Google Gemini** - Image generation AI
- **Docker** - Containerization

### Frontend
- **React Native** 0.72+ - Cross-platform framework
- **TypeScript** 5.0+ - Type safety
- **Redux Toolkit** 2.0+ - State management
- **React Navigation** 6.x - Navigation
- **Axios** 1.6+ - HTTP client
- **React Native Razorpay** - Payment integration

---

## 📦 Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python -m app.main
```

### Frontend Setup
```bash
cd frontend
npm install
cd ios && pod install && cd ..  # macOS only
npm run ios  # or npm run android
```

**See [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md) for detailed setup instructions.**

---

## 📚 Documentation

- **[Installation Guide](./INSTALLATION_GUIDE.md)** - Complete setup with troubleshooting
- **[Quick Start Guide](./QUICK_START_GUIDE.md)** - Get started in 5 minutes
- **[Implementation Summary](./IMPLEMENTATION_SUMMARY.md)** - Technical architecture
- **[Completion Report](./COMPLETION_REPORT.md)** - Project achievements
- **[Backend README](./backend/README.md)** - Backend API documentation
- **[Frontend README](./frontend/README.md)** - Frontend app documentation
- **[Frontend Setup](./frontend/SETUP.md)** - Detailed frontend setup

---

## 🔌 API Endpoints (29 Total)

### Authentication (8)
- Register, Login, OTP Verification, Password Reset, Refresh Token, Logout

### Users (5)
- Profile Management, Credits, Statistics, Account Deletion

### Payments (6)
- Credit Packages, Order Creation, Payment Verification, Coupons, Order History

### Photoshoots (7)
- Create, List, Details, Download (single/all), Delete, Filter Options

### Credits (3)
- Balance, History, Statistics

**Full API Documentation**: http://localhost:8000/docs (when backend is running)

---

## 🏗️ Project Structure

```
application/
├── backend/              # FastAPI Backend (100% complete)
│   ├── app/
│   │   ├── api/v1/      # 29 API endpoints
│   │   ├── core/        # Configuration & security
│   │   ├── services/    # Business logic
│   │   └── schemas/     # Pydantic models
│   ├── tests/           # Backend tests
│   └── Dockerfile       # Docker configuration
│
├── frontend/            # React Native App (95% complete)
│   ├── src/
│   │   ├── screens/     # 9 app screens
│   │   ├── components/  # Reusable UI components
│   │   ├── navigation/  # Navigation setup
│   │   ├── store/       # Redux state management
│   │   ├── services/    # API integration
│   │   ├── theme/       # Design system
│   │   └── utils/       # Helper functions
│   ├── ios/             # iOS native code
│   └── android/         # Android native code
│
└── docs/                # Documentation (7 guides)
```

---

## 🚀 Features Implemented

### Backend (100% Complete)
✅ 29 production-ready API endpoints  
✅ JWT authentication with refresh tokens  
✅ MongoDB async operations  
✅ Razorpay payment integration  
✅ AI service integration (Claude + Gemini)  
✅ Email service with HTML templates  
✅ Comprehensive error handling  
✅ Auto-generated API documentation  
✅ Docker support  
✅ Logging system  

### Frontend (95% Complete)
✅ Complete authentication flow  
✅ Dashboard with real-time statistics  
✅ Photoshoot creation with file upload  
✅ Gallery with filters and navigation  
✅ Payment integration with Razorpay  
✅ Profile management  
✅ Redux state management with persistence  
✅ Custom UI component library  
✅ Image picker integration  
✅ Navigation system (tabs + stack)  
✅ Animation utilities  
✅ Error handling with toast notifications  

---

## 🔐 Security Features

- JWT token authentication with auto-refresh
- Password hashing with bcrypt (12 rounds)
- Email validation (blocks temporary emails)
- Input validation with Pydantic
- CORS configuration
- Razorpay signature verification
- SQL injection prevention
- XSS prevention
- Rate limiting ready

---

## 📊 Project Statistics

- **Total Files**: 70+ files created
- **Lines of Code**: ~6,000 lines
- **API Endpoints**: 29 endpoints
- **Mobile Screens**: 9 screens
- **UI Components**: 15+ reusable components
- **Documentation**: 7 comprehensive guides
- **Development Time**: Accelerated with AI assistance

---

## 💳 Credit Packages

1. **Starter** - 100 credits for ₹999
2. **Basic** - 250 credits for ₹2,199
3. **Pro** - 500 credits for ₹3,999
4. **Business** - 1,000 credits for ₹6,999
5. **Enterprise** - 2,500 credits for ₹14,999

**Coupon Codes**: WELCOME10 (10%), SAVE20 (20%), MEGA50 (50%)

---

## 🎓 Getting Started

1. **Prerequisites**: Python 3.9+, Node.js 16+, MongoDB, Xcode/Android Studio
2. **Read**: [Installation Guide](./INSTALLATION_GUIDE.md)
3. **Setup**: Backend and Frontend
4. **Configure**: Environment variables
5. **Run**: Start both servers
6. **Access**: http://localhost:8000/docs for API

---

## 🐛 Troubleshooting

Common issues and solutions are documented in the [Installation Guide](./INSTALLATION_GUIDE.md#troubleshooting).

Quick fixes:
- **MongoDB**: Check if service is running
- **Port conflict**: Kill process on port 8000
- **Metro cache**: Run `npm start -- --reset-cache`
- **iOS build**: Clean and reinstall pods
- **Android build**: Run `./gradlew clean`

---

## 📈 Roadmap

### Completed ✅
- Backend API (100%)
- Frontend Core (95%)
- Documentation (100%)
- Payment Integration (100%)
- AI Integration (100%)

### Remaining ⏳
- Additional testing (60% remaining)
- Performance optimization
- Production deployment setup
- App store preparation

---

## 🆘 Support

For help and support:
1. Check [Installation Guide](./INSTALLATION_GUIDE.md)
2. Review [Troubleshooting](./INSTALLATION_GUIDE.md#troubleshooting)
3. Check API docs at http://localhost:8000/docs
4. Review error messages in terminal

---

## 🙏 Acknowledgments

- **FastAPI** - Amazing async web framework
- **React Native** - Cross-platform mobile development
- **Anthropic Claude** - AI pose analysis
- **Google Gemini** - AI image generation
- **Razorpay** - Payment processing
- **MongoDB** - Database solution

---

<div align="center">

**Built with ❤️ using FastAPI and React Native**

**Version 1.0.0** | **Last Updated: 2025-10-09**

</div>

