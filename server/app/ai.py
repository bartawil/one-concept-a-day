import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function that sends a prompt to OpenRouter and returns the generated concept
def generate_concept(category: str) -> str:
    prompt = f"""
    Give me a short, clear explanation of an interesting concept in the field of {category}.
    Do not start with the name of the concept. The paragraph should be direct and beginner-friendly.
    """

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/llama-4-scout:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who explains concepts clearly."},
            {"role": "user", "content": prompt.strip()}
        ],
        "max_tokens": 150
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
