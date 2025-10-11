"""
Authentication Tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_register_success(self):
        """Test successful user registration"""
        test_user = {
            "email": f"test_{pytest.test_id}@example.com",
            "password": "TestPass123",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company",
            "phone": "1234567890",
            "is_privacy_accepted": True
        }
        
        response = client.post("/api/v1/auth/register", json=test_user)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "email" in data
    
    def test_register_invalid_email(self):
        """Test registration with invalid email"""
        test_user = {
            "email": "invalid-email",
            "password": "TestPass123",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company",
            "phone": "1234567890",
            "is_privacy_accepted": True
        }
        
        response = client.post("/api/v1/auth/register", json=test_user)
        assert response.status_code == 422
    
    def test_register_weak_password(self):
        """Test registration with weak password"""
        test_user = {
            "email": "test@example.com",
            "password": "123",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company",
            "phone": "1234567890",
            "is_privacy_accepted": True
        }
        
        response = client.post("/api/v1/auth/register", json=test_user)
        assert response.status_code == 400
    
    def test_register_temporary_email(self):
        """Test registration with temporary email"""
        test_user = {
            "email": "test@tempmail.com",
            "password": "TestPass123",
            "first_name": "Test",
            "last_name": "User",
            "company_name": "Test Company",
            "phone": "1234567890",
            "is_privacy_accepted": True
        }
        
        response = client.post("/api/v1/auth/register", json=test_user)
        assert response.status_code == 400
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPassword123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_forgot_password(self):
        """Test forgot password"""
        data = {
            "email": "test@example.com"
        }
        
        response = client.post("/api/v1/auth/forgot-password", json=data)
        assert response.status_code == 200
        assert response.json()["success"] is True


class TestProtectedEndpoints:
    """Test protected endpoints"""
    
    def test_get_profile_without_token(self):
        """Test accessing profile without token"""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
    
    def test_get_profile_with_invalid_token(self):
        """Test accessing profile with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 401


@pytest.fixture(scope="session", autouse=True)
def setup_test_id():
    """Setup unique test ID for each test run"""
    import time
    pytest.test_id = int(time.time())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

