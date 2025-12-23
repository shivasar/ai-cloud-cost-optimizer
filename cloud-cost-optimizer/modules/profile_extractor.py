from .llm_client import query_llm, extract_json_from_text
import json

def extract_project_profile(description):
    """
    Extracts structured project profile from a plain text description using LLM.
    """
    prompt = f"""
    You are a Cloud Architect Helper. 
    Analyze the following project description and extract a structured JSON profile.
    
    Description:
    "{description}"
    
    Output must be a valid JSON object with exactly these fields:
    - name: A suitable name for the project.
    - budget_inr_per_month: The monthly budget in INR (integer). If not specified, estimate a reasonable amount for a small startup or default to 5000.
    - description: The original description provided.
    - tech_stack: A nested object with keys like 'frontend', 'backend', 'database', 'proxy', 'hosting', etc. Fill with inferred or explicit technologies.
    - non_functional_requirements: A list of strings (e.g., "high availability", "low latency") implied or stated.
    
    Return ONLY the JSON object. Do not include any explanation or markdown formatting other than ```json blocks.
    """
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response_text = query_llm(messages, max_tokens=500, temperature=0.1)
        
        if response_text:
            profile = extract_json_from_text(response_text)
            if profile:
                # Ensure budget is an integer
                if 'budget_inr_per_month' in profile:
                    try:
                        profile['budget_inr_per_month'] = int(profile['budget_inr_per_month'])
                    except:
                         profile['budget_inr_per_month'] = 5000 
                return profile
            else:
                print(f"Failed to parse JSON from LLM response: {response_text}")
                return None
        else:
             print(f"LLM returned no response.")
             return None

    except Exception as e:
        print(f"Error during profile extraction: {e}")
        return None
