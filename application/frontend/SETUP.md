# React Native Frontend Setup Guide

This guide will help you set up the React Native frontend for Stylic AI from scratch.

## Prerequisites

### Required Software

1. **Node.js** (v16 or higher)
   ```bash
   node --version
   npm --version
   ```

2. **React Native CLI**
   ```bash
   npm install -g react-native-cli
   ```

3. **Watchman** (macOS only)
   ```bash
   brew install watchman
   ```

### iOS Development (macOS only)

1. **Xcode** (14 or higher)
   - Install from Mac App Store
   - Install Xcode Command Line Tools:
     ```bash
     xcode-select --install
     ```

2. **CocoaPods**
   ```bash
   sudo gem install cocoapods
   ```

### Android Development

1. **Android Studio**
   - Download from https://developer.android.com/studio
   - Install Android SDK (API 33 or higher)
   - Configure ANDROID_HOME environment variable:
     ```bash
     export ANDROID_HOME=$HOME/Library/Android/sdk
     export PATH=$PATH:$ANDROID_HOME/emulator
     export PATH=$PATH:$ANDROID_HOME/tools
     export PATH=$PATH:$ANDROID_HOME/tools/bin
     export PATH=$PATH:$ANDROID_HOME/platform-tools
     ```

2. **Java Development Kit (JDK 11)**
   ```bash
   brew install openjdk@11
   ```

## Step-by-Step Setup

### 1. Initialize React Native Project

```bash
# Navigate to frontend directory
cd application/frontend

# Initialize React Native project with TypeScript
npx react-native init StyLicAI --template react-native-template-typescript

# Move generated files to current directory
mv StyLicAI/* .
mv StyLicAI/.* .
rmdir StyLicAI
```

### 2. Install Dependencies

```bash
# Install all dependencies
npm install

# Or use the provided package.json
npm install
```

### 3. Install iOS Dependencies (macOS only)

```bash
cd ios
pod install
cd ..
```

### 4. Configure Environment Variables

Create `.env` file in the frontend directory:

```bash
# API Configuration
API_BASE_URL=http://localhost:8000/api/v1

# Razorpay Configuration
RAZORPAY_KEY_ID=your_razorpay_key_id

# App Configuration
APP_NAME=Stylic AI
APP_VERSION=1.0.0
```

### 5. Configure TypeScript Path Aliases

The `tsconfig.json` is already configured with path aliases. To make them work with Metro bundler, create/update `babel.config.js`:

```javascript
module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['./src'],
        extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json'],
        alias: {
          '@': './src',
          '@components': './src/components',
          '@screens': './src/screens',
          '@navigation': './src/navigation',
          '@services': './src/services',
          '@store': './src/store',
          '@theme': './src/theme',
          '@utils': './src/utils',
          '@types': './src/types',
          '@constants': './src/constants',
        },
      },
    ],
    'react-native-reanimated/plugin',
  ],
};
```

Install babel plugin:
```bash
npm install --save-dev babel-plugin-module-resolver
```

### 6. Configure React Native Paper Theme

Create `src/App.tsx`:

```typescript
import React from 'react';
import { Provider as PaperProvider } from 'react-native-paper';
import { Provider as ReduxProvider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { store, persistor } from './store/store';
import RootNavigator from './navigation/RootNavigator';
import Toast from 'react-native-toast-message';
import theme from './theme/theme';

const App = () => {
  return (
    <ReduxProvider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <PaperProvider theme={theme}>
          <RootNavigator />
          <Toast />
        </PaperProvider>
      </PersistGate>
    </ReduxProvider>
  );
};

export default App;
```

### 7. Configure Android Permissions

Edit `android/app/src/main/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Add these permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <application
      android:name=".MainApplication"
      android:label="@string/app_name"
      android:icon="@mipmap/ic_launcher"
      android:roundIcon="@mipmap/ic_launcher_round"
      android:allowBackup="false"
      android:theme="@style/AppTheme"
      android:usesCleartextTraffic="true">
      <!-- ... -->
    </application>
</manifest>
```

### 8. Configure iOS Permissions

Edit `ios/StyLicAI/Info.plist`:

```xml
<dict>
    <!-- Add these permissions -->
    <key>NSCameraUsageDescription</key>
    <string>We need access to your camera to upload garment images</string>
    <key>NSPhotoLibraryUsageDescription</key>
    <string>We need access to your photo library to upload images</string>
    <key>NSPhotoLibraryAddUsageDescription</key>
    <string>We need access to save generated images</string>
    <!-- ... -->
</dict>
```

### 9. Run the Application

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

## Project Structure Creation

After setup, create the following directory structure:

```bash
mkdir -p src/{screens,components,navigation,services,store,theme,utils,types,constants}
mkdir -p src/screens/{auth,dashboard,photoshoot,gallery,payment,profile}
mkdir -p src/components/{common,forms,layout}
mkdir -p src/store/slices
mkdir -p assets/{images,fonts,icons}
```

## Next Steps

1. **Create Redux Store** - Set up Redux Toolkit with slices for auth, user, photoshoots, payments
2. **Create Navigation** - Set up React Navigation with auth and main navigators
3. **Create Screens** - Build all required screens (login, register, dashboard, etc.)
4. **Create Components** - Build reusable UI components
5. **Implement Services** - Complete API service implementations
6. **Add Animations** - Implement smooth animations and transitions
7. **Testing** - Write tests for components and services
8. **Build & Deploy** - Create production builds for iOS and Android

## Troubleshooting

### Metro Bundler Issues
```bash
npm start -- --reset-cache
```

### iOS Build Issues
```bash
cd ios
pod deintegrate
pod install
cd ..
```

### Android Build Issues
```bash
cd android
./gradlew clean
cd ..
```

### Clear All Caches
```bash
npm start -- --reset-cache
rm -rf node_modules
rm -rf ios/Pods
rm -rf ios/build
rm -rf android/build
rm -rf android/app/build
npm install
cd ios && pod install && cd ..
```

## Development Tips

1. **Use TypeScript** - Always define types for props and state
2. **Use Hooks** - Prefer functional components with hooks
3. **Memoization** - Use React.memo, useMemo, useCallback for performance
4. **Error Boundaries** - Implement error boundaries for crash handling
5. **Loading States** - Always show loading indicators
6. **Error Handling** - Show user-friendly error messages
7. **Offline Support** - Handle network errors gracefully
8. **Accessibility** - Add accessibility labels and hints

## Resources

- [React Native Documentation](https://reactnative.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [React Native Paper](https://callstack.github.io/react-native-paper/)
- [TypeScript](https://www.typescriptlang.org/)

---

**Need Help?** Check the main README.md or contact the development team.

