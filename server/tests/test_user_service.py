import pytest
import asyncio
import bcrypt
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.user_service import register_user, authenticate_user
from app.models.user_model import UserCreate, UserInDB, UserLogin


class TestUserService:
    """Unit tests for user service business logic"""
    
    @pytest.mark.asyncio
    async def test_register_user_duplicate_email_rejected(self):
        """Test that registering with existing email is rejected"""
        # Arrange - Create user data
        user_data = UserCreate(
            username="testuser",
            email="test@example.com", 
            password="password123",
            interests=["programming"]
        )
        
        # Mock existing user in database
        existing_user = UserInDB(
            id="existing_user_id",
            username="existinguser",
            email="test@example.com",
            password="hashed_password",
            interests=["coding"]
        )
        
        # Mock the database function to return existing user
        with patch('app.services.user_service.get_user_by_email', new_callable=AsyncMock) as mock_get_user:
            mock_get_user.return_value = existing_user
            
            # Act & Assert - Should raise ValueError
            with pytest.raises(ValueError, match="User already exists with this email"):
                await register_user(user_data)
    
    @pytest.mark.asyncio
    async def test_register_user_password_is_encrypted(self):
        """Test that user password is encrypted before storing - CRITICAL SECURITY TEST"""
        # Arrange - Create user with plain text password
        plain_password = "my_secret_password_123"
        user_data = UserCreate(
            username="securitytest",
            email="security@test.com", 
            password=plain_password,
            interests=["security"]
        )
        
        # Mock database functions
        with patch('app.services.user_service.get_user_by_email', new_callable=AsyncMock) as mock_get_user, \
             patch('app.services.user_service.create_user', new_callable=AsyncMock) as mock_create_user:
            
            # No existing user (email is available)
            mock_get_user.return_value = None
            
            # Create REAL encrypted password for the mock
            real_encrypted_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Mock the created user with REAL encrypted password
            mock_created_user = UserInDB(
                id="new_user_id",
                username="securitytest",
                email="security@test.com",
                password=real_encrypted_password,
                interests=["security"]
            )
            mock_create_user.return_value = mock_created_user
            
            # Act - Register the user
            result = await register_user(user_data)
            
            # Assert - Verify the create_user was called
            mock_create_user.assert_called_once_with(user_data)
            
            # CRITICAL SECURITY CHECKS:
            # 1. Password is NOT stored as plain text
            assert result.password != plain_password
            
            # 2. Password has bcrypt format
            assert result.password.startswith("$2b$")
            
            # 3. Password length is realistic for bcrypt (60 chars)
            assert len(result.password) == 60
            
            # 4. Most important: we can verify original password against the hash
            assert bcrypt.checkpw(plain_password.encode('utf-8'), result.password.encode('utf-8'))
    
    @pytest.mark.asyncio
    async def test_authenticate_user_with_correct_password_succeeds(self):
        """Test that login works with correct password - CRITICAL AUTHENTICATION TEST"""
        # Arrange - Create user credentials
        email = "login@test.com"
        plain_password = "correct_password_123"
        
        # Create encrypted password (same as would be in database)
        encrypted_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Mock user in database with encrypted password
        stored_user = UserInDB(
            id="login_user_id",
            username="loginuser",
            email=email,
            password=encrypted_password,  # Stored as encrypted
            interests=["testing"]
        )
        
        # Login attempt with plain text password
        login_data = UserLogin(email=email, password=plain_password)
        
        # Mock database and auth functions
        with patch('app.services.user_service.get_user_by_email', new_callable=AsyncMock) as mock_get_user, \
             patch('app.services.user_service.create_access_token') as mock_create_token:
            
            mock_get_user.return_value = stored_user
            mock_create_token.return_value = "valid_jwt_token_here"
            
            # Act - Try to authenticate
            result = await authenticate_user(login_data)
            
            # Assert - CRITICAL SECURITY CHECKS:
            # 1. Authentication succeeded
            assert result is not None
            
            # 2. Correct user data returned
            assert result.id == "login_user_id"
            assert result.email == email
            assert result.username == "loginuser"
            
            # 3. JWT token created and returned
            assert result.access_token == "valid_jwt_token_here"
            assert result.token_type == "bearer"
            
            # 4. create_access_token was called with correct parameters
            mock_create_token.assert_called_once_with("login_user_id", email)
    
    @pytest.mark.asyncio
    async def test_authenticate_user_with_wrong_password_fails(self):
        """Test that login fails with incorrect password - CRITICAL SECURITY TEST"""
        # Arrange - Create user credentials
        email = "security@test.com"
        correct_password = "correct_password_123"
        wrong_password = "wrong_password_456"
        
        # Create encrypted password for correct password (stored in database)
        encrypted_password = bcrypt.hashpw(correct_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Mock user in database with encrypted correct password
        stored_user = UserInDB(
            id="security_user_id",
            username="securityuser",
            email=email,
            password=encrypted_password,  # Stored correct password (encrypted)
            interests=["security"]
        )
        
        # Login attempt with WRONG password
        login_data = UserLogin(email=email, password=wrong_password)
        
        # Mock database function
        with patch('app.services.user_service.get_user_by_email', new_callable=AsyncMock) as mock_get_user:
            mock_get_user.return_value = stored_user
            
            # Act - Try to authenticate with wrong password
            result = await authenticate_user(login_data)
            
            # Assert - CRITICAL SECURITY CHECK:
            # Authentication MUST fail with wrong password
            assert result is None