import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.security.auth_middleware import get_current_user


class TestAuthMiddleware:
    """Unit tests for authentication middleware - CRITICAL security gateway"""
    
    def test_get_current_user_with_invalid_token_raises_401(self):
        """Test that middleware rejects invalid tokens - MOST CRITICAL SECURITY TEST"""
        # Arrange - Create invalid token credentials
        invalid_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid_token_12345"
        )
        
        # Mock verify_token to return None (invalid token)
        with patch('app.security.auth_middleware.verify_token') as mock_verify:
            mock_verify.return_value = None  # Token verification failed
            
            # Act & Assert - Should raise HTTPException with 401 status
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(invalid_credentials)
            
            # CRITICAL SECURITY CHECKS:
            # 1. Correct HTTP status code (401 Unauthorized)
            assert exc_info.value.status_code == 401
            
            # 2. Correct error message
            assert exc_info.value.detail == "Invalid or expired token"
            
            # 3. Correct WWW-Authenticate header
            assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}
            
            # 4. verify_token was called with the token
            mock_verify.assert_called_once_with("invalid_token_12345")