import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.models.user_model import UserLoginResponse


class TestUserRoutesAPI:
    """Integration tests for User API endpoints - CRITICAL for production readiness"""
    
    def setup_method(self, method):
        """Setup test client for each test"""
        self.client = TestClient(app)
        
    def test_login_endpoint_with_valid_credentials_succeeds(self):
        """Test POST /login endpoint with valid credentials - CRITICAL API TEST"""
        # Arrange - Valid login credentials
        login_data = {
            "email": "api@test.com",
            "password": "valid_password_123"
        }
        
        # Mock the authenticate_user service to return successful authentication
        mock_response = UserLoginResponse(
            id="api_user_id",
            username="apiuser", 
            email="api@test.com",
            interests=["testing"],
            access_token="mock_jwt_token_here",
            token_type="bearer"
        )
        
        # Mock the service function
        with patch('app.api.user_routes.authenticate_user', new_callable=AsyncMock) as mock_auth:
            mock_auth.return_value = mock_response
            
            # Act - Make actual HTTP POST request to /login endpoint
            response = self.client.post("/login", json=login_data)
            
            # Assert - CRITICAL API CHECKS:
            # 1. HTTP status code is 200 (success)
            assert response.status_code == 200
            
            # 2. Response contains correct JSON structure
            response_json = response.json()
            assert "id" in response_json
            assert "username" in response_json
            assert "email" in response_json
            assert "access_token" in response_json
            assert "token_type" in response_json
            
            # 3. Response contains correct data
            assert response_json["id"] == "api_user_id"
            assert response_json["email"] == "api@test.com"
            assert response_json["username"] == "apiuser"
            assert response_json["access_token"] == "mock_jwt_token_here"
            assert response_json["token_type"] == "bearer"
            
            # 4. Service function was called with correct parameters
            mock_auth.assert_called_once()
            called_args = mock_auth.call_args[0][0]
            assert called_args.email == "api@test.com"
            assert called_args.password == "valid_password_123"
            
    def test_login_endpoint_with_invalid_credentials_fails(self):
        """Test POST /login endpoint with invalid credentials - CRITICAL SECURITY TEST"""
        # Arrange - Invalid login credentials
        invalid_login_data = {
            "email": "hacker@evil.com",
            "password": "wrong_password_123"
        }
        
        # Mock the authenticate_user service to return None (failed authentication)
        with patch('app.api.user_routes.authenticate_user', new_callable=AsyncMock) as mock_auth:
            mock_auth.return_value = None  # Authentication failed
            
            # Act - Make actual HTTP POST request to /login endpoint with wrong credentials
            response = self.client.post("/login", json=invalid_login_data)
            
            # Assert - CRITICAL SECURITY CHECKS:
            # 1. HTTP status code is 401 (Unauthorized) - NOT 200!
            assert response.status_code == 401
            
            # 2. Response contains error message, not user data
            response_json = response.json()
            assert "detail" in response_json
            assert response_json["detail"] == "Invalid email or password"
            
            # 3. Response does NOT contain sensitive data
            assert "access_token" not in response_json
            assert "id" not in response_json
            assert "username" not in response_json
            
            # 4. Service function was called (attempted authentication)
            mock_auth.assert_called_once()
            called_args = mock_auth.call_args[0][0]
            assert called_args.email == "hacker@evil.com"
            assert called_args.password == "wrong_password_123"