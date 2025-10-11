# Stylic AI - React Native Frontend

Cross-platform mobile application for Stylic AI built with React Native and TypeScript.

## 📱 Overview

This is the mobile frontend for Stylic AI, providing iOS and Android apps with:
- User authentication and registration
- AI photoshoot generation
- Credit management and payments
- Photoshoot gallery and management
- Order history

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm/yarn
- React Native development environment setup
- iOS: Xcode 14+ (macOS only)
- Android: Android Studio with SDK

### Installation

```bash
# Navigate to frontend directory
cd application/frontend

# Install dependencies
npm install
# or
yarn install

# iOS only - Install pods
cd ios && pod install && cd ..

# Start Metro bundler
npm start
# or
yarn start

# Run on iOS
npm run ios
# or
yarn ios

# Run on Android
npm run android
# or
yarn android
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── screens/              # App screens
│   │   ├── auth/            # Authentication screens
│   │   ├── dashboard/       # Dashboard screen
│   │   ├── photoshoot/      # Photoshoot screens
│   │   ├── gallery/         # Gallery screens
│   │   ├── payment/         # Payment screens
│   │   └── profile/         # Profile screens
│   ├── components/          # Reusable components
│   │   ├── common/          # Common components
│   │   ├── forms/           # Form components
│   │   └── layout/          # Layout components
│   ├── navigation/          # Navigation setup
│   │   ├── AuthNavigator.tsx
│   │   ├── MainNavigator.tsx
│   │   └── RootNavigator.tsx
│   ├── services/            # API services
│   │   ├── api.ts           # API client
│   │   ├── auth.service.ts
│   │   ├── photoshoot.service.ts
│   │   ├── payment.service.ts
│   │   └── user.service.ts
│   ├── store/               # State management
│   │   ├── slices/          # Redux slices
│   │   ├── store.ts         # Redux store
│   │   └── hooks.ts         # Custom hooks
│   ├── theme/               # Design system
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   ├── spacing.ts
│   │   └── theme.ts
│   ├── utils/               # Utilities
│   │   ├── validation.ts
│   │   ├── storage.ts
│   │   └── helpers.ts
│   ├── types/               # TypeScript types
│   │   ├── auth.types.ts
│   │   ├── photoshoot.types.ts
│   │   └── payment.types.ts
│   ├── constants/           # Constants
│   │   └── config.ts
│   └── App.tsx              # Root component
├── assets/                  # Static assets
│   ├── images/
│   ├── fonts/
│   └── icons/
├── android/                 # Android native code
├── ios/                     # iOS native code
├── package.json
├── tsconfig.json
├── babel.config.js
├── metro.config.js
└── README.md
```

## 🎨 Design System

### Colors
Based on the Flask dashboard color scheme:
- Primary: #6366f1 (Indigo)
- Secondary: #8b5cf6 (Purple)
- Success: #10b981 (Green)
- Warning: #f59e0b (Amber)
- Error: #ef4444 (Red)
- Background: #f9fafb (Gray 50)
- Surface: #ffffff (White)
- Text: #111827 (Gray 900)

### Typography
- Font Family: System default (San Francisco on iOS, Roboto on Android)
- Heading 1: 32px, Bold
- Heading 2: 24px, Bold
- Heading 3: 20px, SemiBold
- Body: 16px, Regular
- Caption: 14px, Regular
- Small: 12px, Regular

### Spacing
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- xxl: 48px

## 🔧 Technology Stack

### Core
- **React Native**: 0.72+
- **TypeScript**: 5.0+
- **React**: 18.2+

### Navigation
- **React Navigation**: 6.x
  - Stack Navigator
  - Bottom Tab Navigator
  - Drawer Navigator (optional)

### State Management
- **Redux Toolkit**: 2.0+
- **Redux Persist**: 6.0+
- **React Redux**: 9.0+

### API & Data
- **Axios**: 1.6+
- **React Query** (optional): 5.0+

### UI Components
- **React Native Paper**: 5.x
- **React Native Vector Icons**: 10.x
- **React Native Gesture Handler**: 2.x
- **React Native Reanimated**: 3.x

### Forms & Validation
- **React Hook Form**: 7.x
- **Yup**: 1.x

### Payment
- **Razorpay React Native SDK**: Latest

### Storage
- **AsyncStorage**: Latest
- **React Native MMKV** (optional): Latest

### Image Handling
- **React Native Fast Image**: Latest
- **React Native Image Picker**: Latest

### Other
- **React Native Toast Message**: Latest
- **React Native Modal**: Latest
- **React Native Loading Spinner Overlay**: Latest

## 📱 Screens

### Authentication Flow
1. **Splash Screen** - App loading
2. **Welcome Screen** - Onboarding
3. **Login Screen** - User login
4. **Register Screen** - User registration
5. **OTP Verification Screen** - Email verification
6. **Forgot Password Screen** - Password reset request
7. **Reset Password Screen** - New password entry

### Main App Flow
1. **Dashboard** - Overview and statistics
2. **AI Photoshoot** - Create new photoshoot
3. **Gallery** - View all photoshoots
4. **Photoshoot Details** - View specific photoshoot
5. **Payment** - Purchase credits
6. **Order History** - View past orders
7. **Credit History** - View credit transactions
8. **Profile** - User profile and settings

## 🔐 Authentication

### Token Management
- Access token stored in secure storage
- Refresh token for token renewal
- Automatic token refresh on API calls
- Logout clears all tokens

### Protected Routes
- Automatic redirect to login if not authenticated
- Token validation on app launch
- Persistent login state

## 🌐 API Integration

### Base Configuration
```typescript
const API_BASE_URL = 'http://localhost:8000/api/v1';
// or
const API_BASE_URL = 'https://api.stylic.ai/api/v1';
```

### API Services
- **AuthService**: Authentication operations
- **UserService**: User profile management
- **PhotoshootService**: Photoshoot operations
- **PaymentService**: Payment and credit operations

### Error Handling
- Global error interceptor
- Toast notifications for errors
- Retry logic for failed requests
- Network error handling

## 🎭 Animations

### Screen Transitions
- Fade in/out
- Slide from right/left
- Modal presentation

### Component Animations
- Button press feedback
- Loading spinners
- Skeleton loaders
- Image fade-in
- List item animations

## 🧪 Testing

```bash
# Run tests
npm test
# or
yarn test

# Run tests with coverage
npm test -- --coverage
# or
yarn test --coverage
```

## 📦 Building

### iOS
```bash
# Development build
npm run ios

# Release build
cd ios
xcodebuild -workspace Stylic.xcworkspace -scheme Stylic -configuration Release
```

### Android
```bash
# Development build
npm run android

# Release build
cd android
./gradlew assembleRelease
```

## 🚀 Deployment

### iOS App Store
1. Configure signing in Xcode
2. Archive the app
3. Upload to App Store Connect
4. Submit for review

### Google Play Store
1. Generate signed APK/AAB
2. Upload to Google Play Console
3. Submit for review

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```
API_BASE_URL=http://localhost:8000/api/v1
RAZORPAY_KEY_ID=your_razorpay_key_id
```

### App Configuration
Edit `src/constants/config.ts`:
```typescript
export const config = {
  apiBaseUrl: process.env.API_BASE_URL,
  razorpayKeyId: process.env.RAZORPAY_KEY_ID,
  // ... other config
};
```

## 📝 Development Guidelines

### Code Style
- Use TypeScript for type safety
- Follow React Native best practices
- Use functional components with hooks
- Implement proper error boundaries
- Write meaningful component names

### State Management
- Use Redux for global state
- Use local state for component-specific data
- Implement proper action creators
- Use selectors for derived state

### Performance
- Optimize images
- Use FlatList for long lists
- Implement proper memoization
- Avoid unnecessary re-renders
- Use React.memo for expensive components

## 🐛 Troubleshooting

### Common Issues

**Metro bundler not starting:**
```bash
npm start -- --reset-cache
```

**iOS build fails:**
```bash
cd ios && pod install && cd ..
```

**Android build fails:**
```bash
cd android && ./gradlew clean && cd ..
```

## 📚 Resources

- [React Native Documentation](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [React Native Paper](https://callstack.github.io/react-native-paper/)

## 🤝 Contributing

1. Follow the code style guidelines
2. Write tests for new features
3. Update documentation
4. Create meaningful commit messages

---

**Last Updated**: 2025-10-09
**Version**: 1.0.0

