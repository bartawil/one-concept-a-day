"""
Security utilities for input sanitization and validation.
"""
import re
import html
from bson import ObjectId


def sanitize_string_input(input_str: str, max_length: int = 100) -> str:
    """Sanitize string input to prevent injection attacks"""
    if not isinstance(input_str, str):
        raise ValueError("Input must be a string")
    
    # Remove any MongoDB operators and special characters
    sanitized = re.sub(r'[{}$]', '', input_str)
    
    # Remove path traversal patterns
    sanitized = re.sub(r'\.\.[\\/]', '', sanitized)  # Remove ../ and ..\
    sanitized = re.sub(r'%2e%2e%2f', '', sanitized, flags=re.IGNORECASE)  # Remove URL encoded ../
    sanitized = re.sub(r'%2e%2e%5c', '', sanitized, flags=re.IGNORECASE)  # Remove URL encoded ..\
    sanitized = re.sub(r'\.{4,}', '...', sanitized)  # Limit multiple dots
    
    # Remove dangerous file protocols and paths
    sanitized = re.sub(r'file://', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'\\\\[^\\]+\\', '', sanitized)  # Remove UNC paths
    
    # Remove common system paths
    dangerous_paths = [
        'etc/passwd', 'system32', 'windows', 'config/sam', 
        'var/log', 'boot.ini', 'autoexec.bat'
    ]
    for path in dangerous_paths:
        sanitized = re.sub(re.escape(path), '', sanitized, flags=re.IGNORECASE)
    
    sanitized = sanitized.strip()
    
    if len(sanitized) > max_length:
        raise ValueError(f"Input too long (max {max_length} characters)")
    
    if not sanitized:
        raise ValueError("Input cannot be empty")
        
    return sanitized


def sanitize_html_content(input_str: str, max_length: int = 2000) -> str:
    """Sanitize HTML content to prevent XSS attacks"""
    if not isinstance(input_str, str):
        raise ValueError("Input must be a string")
    
    # Remove dangerous HTML tags and JavaScript
    sanitized = input_str.strip()
    
    # Remove script tags and their content
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove dangerous HTML tags
    dangerous_tags = [
        'script', 'iframe', 'object', 'embed', 'form', 'meta', 'base', 
        'link', 'style', 'svg', 'audio', 'video'
    ]
    
    for tag in dangerous_tags:
        # Remove opening and closing tags
        sanitized = re.sub(f'<{tag}[^>]*>', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(f'</{tag}>', '', sanitized, flags=re.IGNORECASE)
    
    # Remove dangerous attributes
    dangerous_attrs = [
        'onload', 'onerror', 'onclick', 'onmouseover', 'onmouseout',
        'onfocus', 'onblur', 'onsubmit', 'onreset', 'onchange', 'onkeydown',
        'onkeyup', 'onkeypress', 'href', 'src'
    ]
    
    for attr in dangerous_attrs:
        sanitized = re.sub(f'{attr}\\s*=\\s*["\'][^"\']*["\']', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(f'{attr}\\s*=\\s*[^\\s>]*', '', sanitized, flags=re.IGNORECASE)
    
    # Remove javascript: urls
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    
    # HTML escape the remaining content
    sanitized = html.escape(sanitized)
    
    if len(sanitized) > max_length:
        raise ValueError(f"Content too long (max {max_length} characters)")
        
    return sanitized


def sanitize_ai_input(text: str) -> str:
    """Sanitize input for AI prompt to prevent prompt injection"""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Remove potentially dangerous characters and sequences
    sanitized = text.strip()
    
    # Remove prompt injection attempts
    dangerous_patterns = [
        r'ignore.*previous.*instructions?',
        r'forget.*above',
        r'act.*as.*if',
        r'pretend.*to.*be',
        r'system[:\s]',
        r'assistant[:\s]',
        r'user[:\s]',
        r'\[.*\]',
        r'```',
        r'---',
        r'<.*>',
        r'\n\n',
        r'\\n',
    ]
    
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    # Limit to alphanumeric, spaces, and basic punctuation
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-_.,&()]', '', sanitized)
    
    # Limit length and ensure it's not empty
    sanitized = sanitized[:100].strip()
    if not sanitized:
        raise ValueError("Input cannot be empty after sanitization")
    
    return sanitized


def validate_object_id(user_id: str) -> ObjectId:
    """Validate and convert user_id to ObjectId"""
    try:
        if not isinstance(user_id, str) or len(user_id) != 24:
            raise ValueError("Invalid user ID format")
        return ObjectId(user_id)
    except Exception:
        raise ValueError("Invalid user ID")