import re
import json
from typing import Any, Dict
import unicodedata
from openai import AsyncAzureOpenAI
from schema import CarListing
from config import settings

client = AsyncAzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
)

# simple implementation to Prevent Prompt Injection
def sanitize_text(text: str) -> str:
    """Sanitization to prevent prompt injection attempts."""

    # this normalizes Unicode (prevents homoglyph / spacing attacks)
    text = unicodedata.normalize("NFKC", text)

    # Removes code blocks, HTML tags, and script-like content
    text = re.sub(r"```.*?```", "", text, flags=re.S)   # Code blocks
    text = re.sub(r"<[^>]+>", "", text)                 # HTML/XML tags
    text = re.sub(r"(?:javascript:|data:|vbscript:)", "", text, flags=re.I)

    # Remove common prompt injection patterns (expanded & stricter)
    injection_patterns = [
        r"\bignore\b.*\b(instruction|previous)\b",
        r"\b(system|assistant|user|prompt)\s*:",
        r"\bforget\b.*\b(everything|instructions)\b",
        r"\bnew\b.*\binstructions\b",
        r"\byou\s+are\s+now\b",
        r"\boverride\b.*\brules?\b",
        r"\bdisregard\b.*\binstructions?\b",
        r"\bpretend\b.*\b(system|assistant)\b",
    ]
    for pattern in injection_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # Block suspicious encodings (base64 or long gibberish strings)
    if re.search(r"[A-Za-z0-9+/=]{100,}", text):
        raise ValueError("Potential encoded or malicious payload detected")

    # Collapse whitespace and trim length
    text = re.sub(r"\s+", " ", text).strip()

    # Enforce max length (to prevent long injection attempts), we could use when needed
    # MAX_LEN = 2000
    # if len(text) > MAX_LEN:
    #     text = text[:MAX_LEN]

    return text


SYSTEM_PROMPT = """
You are a car‑listing information extractor. Extract ONLY the information needed to fill the JSON schema. 
Do not add explanations. Use `null` for unknown fields.
"""

async def extract_listing(user_text: str) -> Dict[str, Any]:
    """Extract car listing information from user text"""
    # Sanitize input to prevent prompt injection
    sanitized = sanitize_text(user_text)
    
    # Validate that we have meaningful content after sanitization
    if len(sanitized.strip()) < 10:
        raise ValueError("Text too short or contains no meaningful content after sanitization")
    
    try:
        response = await client.chat.completions.create(
            model=settings.AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": sanitized},
            ],
            temperature=0.3,
            max_tokens=800,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "car_listing",
                    "schema": CarListing.model_json_schema()
                }
            }
        )
        
        raw_response = response.choices[0].message.content
        
        if not raw_response:
            raise ValueError("Empty response from OpenAI")
        
        # Clean and extract JSON
        raw_response = raw_response.strip()
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
        else:
            json_str = raw_response
        
        # Parse JSON
        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError:
            # Clean common JSON issues and retry
            json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
            json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas in arrays
            parsed_json = json.loads(json_str)
        
        # Validate using Pydantic
        validated = CarListing(**parsed_json)
        return validated.dict()
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned: {e}\nRaw: {raw_response}")
    except Exception as e:
        raise ValueError(f"Failed to extract car information: {str(e)}")
    