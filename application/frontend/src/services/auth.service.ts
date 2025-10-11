/**
 * Authentication Service
 */

import api from './api';
import {
  RegisterRequest,
  RegisterResponse,
  LoginRequest,
  LoginResponse,
  VerifyOTPRequest,
  VerifyOTPResponse,
  ResendOTPRequest,
  ResendOTPResponse,
  ForgotPasswordRequest,
  ForgotPasswordResponse,
  ResetPasswordRequest,
  ResetPasswordResponse,
  RefreshTokenRequest,
  RefreshTokenResponse,
} from '../types/auth.types';

class AuthService {
  /**
   * Register new user
   */
  async register(data: RegisterRequest): Promise<RegisterResponse> {
    const response = await api.post<RegisterResponse>('/auth/register', data);
    return response.data;
  }

  /**
   * Login user
   */
  async login(data: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login', data);
    return response.data;
  }

  /**
   * Verify OTP
   */
  async verifyOTP(data: VerifyOTPRequest): Promise<VerifyOTPResponse> {
    const response = await api.post<VerifyOTPResponse>('/auth/verify-otp', data);
    return response.data;
  }

  /**
   * Resend OTP
   */
  async resendOTP(data: ResendOTPRequest): Promise<ResendOTPResponse> {
    const response = await api.post<ResendOTPResponse>('/auth/resend-otp', data);
    return response.data;
  }

  /**
   * Forgot password
   */
  async forgotPassword(data: ForgotPasswordRequest): Promise<ForgotPasswordResponse> {
    const response = await api.post<ForgotPasswordResponse>('/auth/forgot-password', data);
    return response.data;
  }

  /**
   * Reset password
   */
  async resetPassword(data: ResetPasswordRequest): Promise<ResetPasswordResponse> {
    const response = await api.post<ResetPasswordResponse>('/auth/reset-password', data);
    return response.data;
  }

  /**
   * Refresh access token
   */
  async refreshToken(data: RefreshTokenRequest): Promise<RefreshTokenResponse> {
    const response = await api.post<RefreshTokenResponse>('/auth/refresh', data);
    return response.data;
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    // Clear tokens from storage
    // This is handled in the Redux slice
  }
}

export default new AuthService();

