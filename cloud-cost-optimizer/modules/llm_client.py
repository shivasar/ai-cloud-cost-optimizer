import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
# Switching to Zephyr-7b-beta which is highly reliable on free tier
# Using OpenAI-compatible endpoint on Hugging Face Router
API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

def query_llm(messages, max_tokens=1000, temperature=0.1, retries=3):
    """
    Sends a chat completion request to the Hugging Face Router.
    Args:
        messages: List of dicts, e.g. [{"role": "user", "content": "..."}]
        max_tokens: Max tokens to generate
        temperature: Creativity (0.0 - 1.0)
        retries: Number of retries on failure
        
    Returns:
        str: The generated text content from the assistant.
    """
    if not HF_API_TOKEN:
        raise ValueError("HF_API_TOKEN not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # OpenAI format extraction
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                return content
            else:
                raise ValueError(f"Unexpected response format: {data}")
                
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                error_msg = f"Failed to query LLM after {retries} attempts: {e}"
                if 'response' in locals() and response is not None:
                     error_msg += f"\nResponse Body: {response.text}"
                raise RuntimeError(error_msg)
            import time
            time.sleep(2) # Wait before retry

def extract_json_from_text(text):
    """
    Extracts a JSON object from a string that might contain other text.
    Handles markdown code blocks.
    """
    # Try to find JSON inside markdown blocks (with or without 'json' language identifier)
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # If no markdown, try to find the first '{' or '[' and last '}' or ']'
        # Find start indices
        start_obj = text.find('{')
        start_list = text.find('[')
        
        # Determine strict start index
        start = -1
        if start_obj != -1 and start_list != -1:
            start = min(start_obj, start_list)
        elif start_obj != -1:
            start = start_obj
        elif start_list != -1:
            start = start_list
            
        if start == -1:
            return None
            
        # Find end indices (search from right)
        end_obj = text.rfind('}')
        end_list = text.rfind(']')
        
        end = -1
        if end_obj != -1 and end_list != -1:
            end = max(end_obj, end_list)
        elif end_obj != -1:
            end = end_obj
        elif end_list != -1:
            end = end_list
            
        if end == -1 or end < start:
            return None
            
        json_str = text[start:end+1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

if __name__ == "__main__":
    # Test block
    print("Testing LLM connection...")
    try:
        test_prompt = "Generate a simple JSON object with a key 'message' and value 'Hello World'."
        messages = [{"role": "user", "content": test_prompt}]
        
        print("Sending request...")
        result_text = query_llm(messages, max_tokens=100, temperature=0.1)
        
        print("Result Text:", result_text)
        extracted = extract_json_from_text(result_text)
        print("Extracted JSON:", extracted)
            
    except Exception as e:
        print(f"Error: {e}")
