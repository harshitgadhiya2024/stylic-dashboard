# Stylic AI - Complete Installation Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Environment Configuration](#environment-configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: At least 5GB free space

### Required Software

#### For Backend
- **Python**: 3.9 or higher
  ```bash
  python --version  # Should show 3.9+
  ```
- **pip**: Latest version
  ```bash
  pip --version
  ```
- **MongoDB**: 4.4 or higher (local or cloud)
  ```bash
  mongosh --version
  ```

#### For Frontend
- **Node.js**: 16 or higher
  ```bash
  node --version  # Should show v16+
  ```
- **npm**: 8 or higher
  ```bash
  npm --version
  ```
- **Xcode**: Latest version (macOS only, for iOS development)
- **Android Studio**: Latest version (for Android development)
- **CocoaPods**: Latest version (macOS only)
  ```bash
  pod --version
  ```

---

## 🔙 Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd application/backend
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use any text editor
```

**Required Environment Variables:**
```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/stylic_ai
# Or use MongoDB Atlas:
# MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/stylic_ai

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
REFRESH_SECRET_KEY=your-refresh-secret-key-change-this-too
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email Configuration (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Stylic AI

# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret

# AI Service API Keys
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-ai-key
OPENAI_API_KEY=sk-your-openai-key

# Application Configuration
ENVIRONMENT=development
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19006
```

### Step 5: Verify MongoDB Connection
```bash
# Test MongoDB connection
mongosh

# Or if using MongoDB Atlas, test with:
mongosh "mongodb+srv://cluster.mongodb.net/stylic_ai" --username your-username
```

### Step 6: Run Backend Server
```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 7: Verify Backend is Running
Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📱 Frontend Setup

### Step 1: Navigate to Frontend Directory
```bash
cd application/frontend
```

### Step 2: Install Node Dependencies
```bash
npm install
# or
yarn install
```

### Step 3: Install iOS Dependencies (macOS only)
```bash
cd ios
pod install
cd ..
```

### Step 4: Configure Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
nano .env
```

**Required Environment Variables:**
```env
# API Configuration
API_BASE_URL=http://localhost:8000/api/v1
# For Android emulator, use: http://10.0.2.2:8000/api/v1
# For iOS simulator, use: http://localhost:8000/api/v1
# For physical device, use your computer's IP: http://192.168.x.x:8000/api/v1

# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_test_your_key_id

# App Configuration
APP_NAME=Stylic AI
APP_VERSION=1.0.0
```

### Step 5: Setup React Native Development Environment

#### For iOS (macOS only)
1. Install Xcode from App Store
2. Install Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
3. Install CocoaPods:
   ```bash
   sudo gem install cocoapods
   ```

#### For Android
1. Download and install Android Studio
2. Install Android SDK (API 31 or higher)
3. Set up environment variables:
   ```bash
   # Add to ~/.bash_profile or ~/.zshrc
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/tools/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```
4. Create Android Virtual Device (AVD) in Android Studio

### Step 6: Run Frontend Application

#### Start Metro Bundler
```bash
npm start
# or
npx react-native start
```

#### Run on iOS (macOS only)
```bash
# In a new terminal
npm run ios
# or
npx react-native run-ios

# To run on specific device:
npx react-native run-ios --device "iPhone 14 Pro"
```

#### Run on Android
```bash
# Start Android emulator first, then:
npm run android
# or
npx react-native run-android
```

---

## 🔐 Environment Configuration

### Getting API Keys

#### 1. MongoDB Atlas (Free Tier)
1. Visit https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create cluster
4. Get connection string

#### 2. Gmail App Password
1. Enable 2-Factor Authentication
2. Go to Google Account Settings
3. Security → App Passwords
4. Generate password for "Mail"

#### 3. Razorpay (Test Mode)
1. Visit https://razorpay.com
2. Sign up for account
3. Go to Settings → API Keys
4. Generate Test Keys

#### 4. Anthropic Claude API
1. Visit https://console.anthropic.com
2. Create account
3. Generate API key

#### 5. Google AI (Gemini)
1. Visit https://makersuite.google.com/app/apikey
2. Create API key

---

## 🚀 Running the Application

### Complete Startup Sequence

1. **Start MongoDB** (if running locally)
   ```bash
   # macOS
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

2. **Start Backend**
   ```bash
   cd application/backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python -m app.main
   ```

3. **Start Frontend**
   ```bash
   # Terminal 1: Metro Bundler
   cd application/frontend
   npm start
   
   # Terminal 2: iOS or Android
   npm run ios    # or npm run android
   ```

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: MongoDB Connection Error**
```bash
# Check if MongoDB is running
mongosh

# Start MongoDB service
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

**Issue: Port 8000 Already in Use**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or change port in backend
uvicorn app.main:app --reload --port 8001
```

**Issue: Module Not Found**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Issue: Metro Bundler Cache**
```bash
# Clear cache
npm start -- --reset-cache
```

**Issue: iOS Build Fails**
```bash
cd ios
rm -rf Pods Podfile.lock
pod deintegrate
pod install
cd ..
```

**Issue: Android Build Fails**
```bash
cd android
./gradlew clean
cd ..
```

**Issue: Cannot Connect to Backend**
- iOS Simulator: Use `http://localhost:8000`
- Android Emulator: Use `http://10.0.2.2:8000`
- Physical Device: Use your computer's IP `http://192.168.x.x:8000`

**Issue: Image Picker Not Working**
- iOS: Add permissions to `ios/StylichAI/Info.plist`:
  ```xml
  <key>NSPhotoLibraryUsageDescription</key>
  <string>We need access to your photos</string>
  <key>NSCameraUsageDescription</key>
  <string>We need access to your camera</string>
  ```
- Android: Permissions already added in `AndroidManifest.xml`

---

## ✅ Verification Checklist

- [ ] MongoDB is running and accessible
- [ ] Backend server starts without errors
- [ ] API documentation loads at http://localhost:8000/docs
- [ ] Frontend Metro bundler starts successfully
- [ ] App launches on iOS/Android
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Can view dashboard
- [ ] Can navigate between screens

---

## 📚 Additional Resources

- **Backend README**: `application/backend/README.md`
- **Frontend README**: `application/frontend/README.md`
- **Quick Start Guide**: `application/QUICK_START_GUIDE.md`
- **API Documentation**: http://localhost:8000/docs (when running)

---

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Check logs in terminal
4. Verify all environment variables are set correctly
5. Ensure all prerequisites are installed

---

**Installation Complete! 🎉**

You're now ready to use Stylic AI!

