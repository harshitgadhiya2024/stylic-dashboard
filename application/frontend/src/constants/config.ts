/**
 * Application Configuration
 */

export const config = {
  // API Configuration
  apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000/api/v1',
  apiTimeout: 30000, // 30 seconds
  
  // Razorpay Configuration
  razorpayKeyId: process.env.RAZORPAY_KEY_ID || '',
  
  // App Configuration
  appName: 'Stylic AI',
  appVersion: '1.0.0',
  
  // Storage Keys
  storageKeys: {
    accessToken: '@stylic:accessToken',
    refreshToken: '@stylic:refreshToken',
    user: '@stylic:user',
    theme: '@stylic:theme',
  },
  
  // Pagination
  defaultPageSize: 20,
  maxPageSize: 100,
  
  // File Upload
  maxFileSize: 10 * 1024 * 1024, // 10MB
  allowedImageTypes: ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
  
  // Validation
  minPasswordLength: 8,
  maxPasswordLength: 128,
  otpLength: 6,
  otpExpiryMinutes: 10,
  
  // Credits
  minCreditPurchase: 10,
  maxCreditPurchase: 10000,
  
  // Photoshoot
  maxPoseImages: 10,
  maxGarmentImages: 2,
  
  // Toast Duration
  toastDuration: 3000, // 3 seconds
  
  // Retry Configuration
  maxRetries: 3,
  retryDelay: 1000, // 1 second
  
  // Cache Duration
  cacheDuration: 5 * 60 * 1000, // 5 minutes
};

export default config;

