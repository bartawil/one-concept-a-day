import os
import re
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_specific_concept(category: str, seen_terms: list[str]) -> dict:
    if not category:
        raise ValueError("Category is required")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OpenRouter API key")
    
    """
    Generates a specific concept and its explanation for a given category,
    excluding previously seen terms.
    Returns a dictionary: { 'term': ..., 'explanation': ... }
    """

    blacklist = ", ".join(seen_terms) if seen_terms else "none"
    prompt = f"""
    Pick a specific, interesting technical term or key concept from the field of {category},
    that is NOT one of the following: {blacklist}.

    Then write a short, clear explanation for it.

    Format your answer like this:
    Term: <term>
    <Explanation in 2–3 sentences>

    Avoid vague or generic answers. Avoid repeating general overviews of the field itself.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": os.getenv("OPENROUTER_MODEL"),
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who explains specific concepts clearly."},
            {"role": "user", "content": prompt.strip()}
        ],
        "max_tokens": 300
    }
    
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        if not content:
            raise ValueError("Empty response from model")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch concept from model: {e}")


    # Try parsing "Term: <term>\n<explanation>"
    match = re.search(r"Term:\s*(.+?)\n+(.+)", content, re.DOTALL)
    if match:
        term = match.group(1).strip()
        explanation = match.group(2).strip()
        return {"term": term, "explanation": explanation}

    # Fallback: try parsing "Term: explanation" (everything in one line)
    match = re.match(r"(Term:)?\s*(.+?)\s*:\s*(.+)", content, re.DOTALL)
    if match:
        term = match.group(2).strip()
        explanation = match.group(3).strip()
        return {"term": term, "explanation": explanation}

    # Final fallback: return raw
    return {"term": category.strip(), "explanation": content}
