import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
import jwt
import os
from app.security.auth_service import create_access_token, verify_token


class TestAuthService:
    """Unit tests for authentication service"""
    
    def setup_method(self, method):
        """Setup test environment before each test"""
        self.test_secret = "test_secret_key_123"
        
    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})  
    def test_create_access_token_valid(self):
        """Test creating a valid JWT token"""
        # Arrange
        user_id = "test_user_123"
        email = "test@example.com"
        
        # Mock the auth_service module directly to ensure consistent secret
        with patch('app.security.auth_service.SECRET_KEY', self.test_secret):
            # Act
            token = create_access_token(user_id, email)
            
            # Assert
            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 0
            
            # Verify token can be decoded manually
            payload = jwt.decode(token, self.test_secret, algorithms=["HS256"])
            assert payload["user_id"] == user_id
            assert payload["email"] == email
            assert "exp" in payload
            assert "iat" in payload

    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})
    def test_verify_token_valid(self):
        """Test verifying a valid JWT token"""
        # Arrange
        user_id = "test_user_456"
        email = "user@test.com"
        token = create_access_token(user_id, email)
        
        # Act
        payload = verify_token(token)
        
        # Assert
        assert payload is not None
        assert payload["user_id"] == user_id
        assert payload["email"] == email
        
    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})
    def test_verify_token_invalid(self):
        """Test verifying an invalid JWT token"""
        # Arrange
        invalid_token = "invalid.token.here"
        
        # Act
        payload = verify_token(invalid_token)
        
        # Assert
        assert payload is None
        
    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})
    def test_verify_token_expired(self):
        """Test verifying an expired JWT token"""
        # Arrange - create an expired token
        user_id = "test_user_789"
        email = "expired@test.com"
        
        # Create token that expired 1 hour ago
        past_time = datetime.now(timezone.utc) - timedelta(hours=25)  # 25 hours ago
        expired_payload = {
            "user_id": user_id,
            "email": email,
            "exp": past_time,
            "iat": past_time - timedelta(hours=1)
        }
        expired_token = jwt.encode(expired_payload, self.test_secret, algorithm="HS256")
        
        # Act
        payload = verify_token(expired_token)
        
        # Assert
        assert payload is None

    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})
    def test_token_contains_correct_fields(self):
        """Test that token contains all required fields"""
        # Arrange
        user_id = "field_test_user"
        email = "fields@test.com"
        
        # Act
        token = create_access_token(user_id, email)
        payload = verify_token(token)
        
        # Assert
        assert "user_id" in payload
        assert "email" in payload
        assert "exp" in payload  # expiration time
        assert "iat" in payload  # issued at time
        
        # Verify expiration is in the future
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        assert exp_time > now

    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})
    def test_verify_token_wrong_secret(self):
        """Test verifying token with wrong secret key"""
        # Arrange
        user_id = "wrong_secret_user"
        email = "wrong@test.com"
        
        # Create token with different secret
        wrong_secret = "wrong_secret_key"
        wrong_payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc)
        }
        wrong_token = jwt.encode(wrong_payload, wrong_secret, algorithm="HS256")
        
        # Act
        payload = verify_token(wrong_token)
        
        # Assert
        assert payload is None

    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})
    def test_token_expiration_time_correct(self):
        """Test that token expires approximately after 24 hours"""
        # Arrange
        user_id = "expiration_test_user"
        email = "expiration@test.com"
        before_creation = datetime.now(timezone.utc)
        
        # Act
        token = create_access_token(user_id, email)
        payload = verify_token(token)
        after_creation = datetime.now(timezone.utc)
        
        # Assert
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_exp_min = before_creation + timedelta(hours=23, minutes=59)  # Allow 1 minute margin
        expected_exp_max = after_creation + timedelta(hours=24, minutes=1)   # Allow 1 minute margin
        
        assert expected_exp_min <= exp_time <= expected_exp_max

    @patch.dict(os.environ, {"JWT_SECRET_KEY": "test_secret_key_123"})
    def test_empty_user_data(self):
        """Test creating token with empty user data raises ValueError"""
        # Arrange
        user_id = ""
        email = ""
        
        # Act & Assert - Should raise ValueError for empty data
        with pytest.raises(ValueError) as exc_info:
            create_access_token(user_id, email)
        
        # Assert correct error message
        assert str(exc_info.value) == "user_id and email are required"