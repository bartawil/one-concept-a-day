import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from app.db.user_repository import add_interest, remove_interest
from app.models.user_model import UserInDB


class TestNoSQLInjectionAttack:
    """Test that simulates a real NoSQL injection attack attempt"""
    
    @pytest.mark.asyncio
    async def test_nosql_injection_attack_simulation(self):
        """
        Simulate a real NoSQL injection attack where an attacker tries to:
        1. Bypass authentication 
        2. Access other users' data
        3. Modify database queries
        """
        print("\n[SECURITY TEST] Simulating NoSQL injection attack...")
        
        # Valid user for the test
        target_user_id = "507f1f77bcf86cd799439011"
        
        # Mock a valid user exists
        mock_user = UserInDB(
            id=target_user_id,
            username="victim_user",
            email="victim@example.com", 
            password="hashed_password",
            interests=["programming", "security"]
        )
        
        # ATTACK PAYLOADS - These are real attack vectors
        attack_payloads = [
            # 1. Try to inject MongoDB operators
            {"$ne": None},  # "Not equals null" - tries to match any value
            
            # 2. Try to execute arbitrary code  
            {"$where": "this.username === 'admin'"},
            
            # 3. Try to access sensitive fields
            {"$regex": ".*", "$options": "i"},
            
            # 4. Try to bypass validation with nested objects
            {"interest": {"$exists": True}},
            
            # 5. String-based injection attempts
            "programming'; DROP TABLE users; --",
            "programming${ne}null",
            "test{$where: 'this.password'}",
            "value${gt}",
            '{"$ne": null}',
        ]
        
        with patch('app.db.user_repository.get_user_by_id', new_callable=AsyncMock) as mock_get_user, \
             patch('app.db.user_repository.db') as mock_db:
            
            mock_get_user.return_value = mock_user
            mock_update = AsyncMock()
            mock_db.__getitem__.return_value.update_one = mock_update
            
            attack_blocked_count = 0
            
            print(f"Testing {len(attack_payloads)} different attack vectors...")
            
            # Test each attack payload
            for i, payload in enumerate(attack_payloads, 1):
                print(f"\nAttack #{i}: {payload}")
                
                try:
                    # Try the attack
                    await add_interest(target_user_id, payload)
                    
                    # If we get here, check what was actually sent to DB
                    if mock_update.called:
                        call_args = mock_update.call_args
                        db_payload = call_args[0][1]["$addToSet"]["interests"]
                        
                        # Verify the payload was sanitized
                        if isinstance(db_payload, str):
                            # String payloads should have dangerous chars removed
                            dangerous_chars = ['$', '{', '}']
                            has_dangerous = any(char in db_payload for char in dangerous_chars)
                            
                            if not has_dangerous:
                                print(f"   [BLOCKED] Attack sanitized to: '{db_payload}'")
                                attack_blocked_count += 1
                            else:
                                print(f"   [BREACH] Dangerous payload reached DB: {db_payload}")
                        else:
                            print(f"   [CRITICAL BREACH] Non-string payload reached DB: {db_payload}")
                    
                    mock_update.reset_mock()
                    
                except ValueError as e:
                    # This is good - the attack was blocked at validation level
                    print(f"   [BLOCKED] Attack blocked at validation: {str(e)}")
                    attack_blocked_count += 1
                    
                except Exception as e:
                    print(f"   [ERROR] Unexpected error: {str(e)}")
            
            # FINAL SECURITY ASSESSMENT
            print(f"\nSECURITY ASSESSMENT RESULTS:")
            print(f"   Total attacks tested: {len(attack_payloads)}")
            print(f"   Attacks blocked: {attack_blocked_count}")
            print(f"   Success rate: {(attack_blocked_count/len(attack_payloads)*100):.1f}%")
            
            if attack_blocked_count == len(attack_payloads):
                print("   [SECURE] ALL ATTACKS BLOCKED - System is secure")
            elif attack_blocked_count >= len(attack_payloads) * 0.8:
                print("   [WARNING] Mostly secure - Some vulnerabilities detected")
            else:
                print("   [CRITICAL] System has serious security issues")
            
            # Test should pass only if ALL attacks were blocked
            assert attack_blocked_count == len(attack_payloads), f"Security breach detected! Only {attack_blocked_count}/{len(attack_payloads)} attacks were blocked"

    @pytest.mark.asyncio  
    async def test_advanced_nosql_injection_with_user_id(self):
        """Test injection attacks on the user_id parameter"""
        print("\n[SECURITY TEST] Testing user_id injection attacks...")
        
        # Attack payloads for user_id field
        malicious_user_ids = [
            "507f1f77bcf86cd799439011'; DROP TABLE users; --",
            {"$ne": None},
            ["507f1f77bcf86cd799439011"],
            "507f1f77bcf86cd79943901",  # Invalid length
            "507f1f77bcf86cd79943901g",  # Invalid hex char
            None,
            "",
            "invalid_format",
        ]
        
        blocked_attacks = 0
        
        for i, malicious_id in enumerate(malicious_user_ids, 1):
            print(f"\nUser ID Attack #{i}: {malicious_id}")
            
            try:
                await add_interest(malicious_id, "test_interest")
                print(f"   [BREACH] Invalid user_id was accepted: {malicious_id}")
            except ValueError as e:
                print(f"   [BLOCKED] Attack blocked: {str(e)}")
                blocked_attacks += 1
            except Exception as e:
                print(f"   [BLOCKED] Attack caused error: {str(e)}")
                blocked_attacks += 1
        
        print(f"\nUser ID attacks blocked: {blocked_attacks}/{len(malicious_user_ids)}")
        
        # All user_id attacks should be blocked
        assert blocked_attacks == len(malicious_user_ids), "Some user_id injection attacks were not blocked!"

if __name__ == "__main__":
    # Run just this test file
    pytest.main([__file__, "-v", "-s"])