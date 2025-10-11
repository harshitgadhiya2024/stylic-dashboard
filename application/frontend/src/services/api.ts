/**
 * API Client Configuration
 */

import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import config from '../constants/config';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: config.apiTimeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem(config.storageKeys.accessToken);
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors and token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    
    // Handle 401 Unauthorized - Token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh token
        const refreshToken = await AsyncStorage.getItem(config.storageKeys.refreshToken);
        
        if (refreshToken) {
          const response = await axios.post(
            `${config.apiBaseUrl}/auth/refresh`,
            { refresh_token: refreshToken }
          );
          
          const { access_token } = response.data;
          
          // Save new token
          await AsyncStorage.setItem(config.storageKeys.accessToken, access_token);
          
          // Retry original request with new token
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
          }
          
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed - Clear tokens and redirect to login
        await AsyncStorage.multiRemove([
          config.storageKeys.accessToken,
          config.storageKeys.refreshToken,
          config.storageKeys.user,
        ]);
        
        // TODO: Navigate to login screen
        // NavigationService.navigate('Login');
        
        return Promise.reject(refreshError);
      }
    }
    
    // Handle other errors
    return Promise.reject(error);
  }
);

// API Error Handler
export const handleApiError = (error: any): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<any>;
    
    // Network error
    if (!axiosError.response) {
      return 'Network error. Please check your internet connection.';
    }
    
    // Server error with message
    if (axiosError.response?.data?.detail) {
      return axiosError.response.data.detail;
    }
    
    if (axiosError.response?.data?.message) {
      return axiosError.response.data.message;
    }
    
    // HTTP status errors
    switch (axiosError.response?.status) {
      case 400:
        return 'Invalid request. Please check your input.';
      case 401:
        return 'Unauthorized. Please login again.';
      case 403:
        return 'Access denied.';
      case 404:
        return 'Resource not found.';
      case 422:
        return 'Validation error. Please check your input.';
      case 500:
        return 'Server error. Please try again later.';
      case 503:
        return 'Service unavailable. Please try again later.';
      default:
        return 'An error occurred. Please try again.';
    }
  }
  
  return 'An unexpected error occurred.';
};

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T = any> {
  data: T[];
  total: number;
  skip: number;
  limit: number;
}

// Export configured axios instance
export default api;

