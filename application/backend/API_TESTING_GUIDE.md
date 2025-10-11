# API Testing Guide

Complete guide for testing Stylic AI Backend APIs.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.stylic.ai` (when deployed)

## Authentication Flow

### 1. Register New User

**Endpoint**: `POST /api/v1/auth/register`

**Request**:
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "company_name": "Doe Enterprises",
  "phone": "+1234567890",
  "is_privacy_accepted": true
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "OTP sent successfully. Please check your email.",
  "email": "john.doe@example.com"
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "Doe Enterprises",
    "phone": "+1234567890",
    "is_privacy_accepted": true
  }'
```

### 2. Verify OTP

**Endpoint**: `POST /api/v1/auth/verify-otp?email={email}`

**Request**:
```json
{
  "otp": 123456
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "john.doe@example.com",
    "first_name": "john",
    "last_name": "doe",
    "company_name": "doe enterprises",
    "phone": "+1234567890",
    "credit": 5,
    "plan": "",
    "role": "company",
    "is_active": true,
    "created_at": "2025-10-09T10:00:00",
    "updated_at": "2025-10-09T10:00:00"
  }
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/verify-otp?email=john.doe@example.com" \
  -H "Content-Type: application/json" \
  -d '{
    "otp": 123456
  }'
```

### 3. Resend OTP

**Endpoint**: `POST /api/v1/auth/resend-otp?email={email}`

**Response** (200 OK):
```json
{
  "success": true,
  "message": "OTP sent successfully. Please check your email."
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/resend-otp?email=john.doe@example.com"
```

### 4. Login

**Endpoint**: `POST /api/v1/auth/login`

**Request**:
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "john.doe@example.com",
    "first_name": "john",
    "last_name": "doe",
    "company_name": "doe enterprises",
    "phone": "+1234567890",
    "credit": 5,
    "plan": "",
    "role": "company",
    "is_active": true,
    "created_at": "2025-10-09T10:00:00",
    "updated_at": "2025-10-09T10:00:00"
  }
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123"
  }'
```

### 5. Forgot Password

**Endpoint**: `POST /api/v1/auth/forgot-password`

**Request**:
```json
{
  "email": "john.doe@example.com"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Reset link sent successfully. Please check your email."
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/forgot-password" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com"
  }'
```

### 6. Reset Password

**Endpoint**: `POST /api/v1/auth/reset-password`

**Request**:
```json
{
  "email": "john.doe@example.com",
  "password": "NewSecurePass123",
  "confirm_password": "NewSecurePass123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password updated successfully"
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/reset-password" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "NewSecurePass123",
    "confirm_password": "NewSecurePass123"
  }'
```

### 7. Change Password (Authenticated)

**Endpoint**: `POST /api/v1/auth/change-password`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Request**:
```json
{
  "password": "NewSecurePass456",
  "confirm_password": "NewSecurePass456"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Password updated successfully"
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/change-password" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "password": "NewSecurePass456",
    "confirm_password": "NewSecurePass456"
  }'
```

### 8. Logout (Authenticated)

**Endpoint**: `POST /api/v1/auth/logout`

**Headers**:
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Using Access Tokens

After login or OTP verification, you'll receive an `access_token`. Use this token in the `Authorization` header for all authenticated requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email not valid. Temporary email addresses are not allowed."
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "User account is disabled"
}
```

### 422 Validation Error
```json
{
  "success": false,
  "error": "Validation error",
  "details": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "message": "An error occurred"
}
```

## Testing with Postman

1. Import the API collection (to be created)
2. Set environment variables:
   - `base_url`: `http://localhost:8000`
   - `access_token`: (will be set automatically after login)
3. Run the authentication flow
4. Use the access token for authenticated requests

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(
    f"{BASE_URL}/api/v1/auth/register",
    json={
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "company_name": "Test Co",
        "phone": "1234567890",
        "is_privacy_accepted": True
    }
)
print(response.json())

# Verify OTP (get OTP from email)
otp = input("Enter OTP: ")
response = requests.post(
    f"{BASE_URL}/api/v1/auth/verify-otp",
    params={"email": "test@example.com"},
    json={"otp": int(otp)}
)
data = response.json()
access_token = data["access_token"]
print(f"Access Token: {access_token}")

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(
    f"{BASE_URL}/api/v1/users/me",
    headers=headers
)
print(response.json())
```

## Next Steps

- Test user management endpoints (to be implemented)
- Test photoshoot endpoints (to be implemented)
- Test payment endpoints (to be implemented)
- Test credit management endpoints (to be implemented)

---

**Note**: Replace `YOUR_ACCESS_TOKEN` with the actual token received from login/verify-otp endpoints.

