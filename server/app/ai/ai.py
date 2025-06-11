import os
import requests
from dotenv import load_dotenv
from app.security.security import sanitize_ai_input

# Load environment variables
load_dotenv()

def generate_concept(category: str) -> str:
    if not category:
        raise ValueError("Category is required")
    
    # Sanitize the category input to prevent prompt injection
    try:
        safe_category = sanitize_ai_input(category)
    except ValueError as e:
        raise ValueError(f"Invalid category: {str(e)}")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OpenRouter API key")
    
    # Use safe_category in a controlled way
    prompt = f"""
    Give me a short, clear explanation of an interesting concept in the field of {safe_category}.
    Do not start with the name of the concept. The paragraph should be direct and beginner-friendly.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": os.getenv("OPENROUTER_MODEL"),
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who explains concepts clearly. Only respond with educational content about the requested topic."},
            {"role": "user", "content": prompt.strip()}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not content:
            raise ValueError("Empty response from model")
        return content
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch concept from model: {e}")

