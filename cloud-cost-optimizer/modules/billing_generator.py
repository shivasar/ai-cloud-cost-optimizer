from .llm_client import query_llm, extract_json_from_text
import json
import random

def generate_synthetic_billing(profile):
    """
    Generates realistic, budget-aware synthetic cloud billing data based on the project profile.
    """
    if not profile:
        return None

    budget = profile.get('budget_inr_per_month', 5000)
    tech_stack = json.dumps(profile.get('tech_stack', {}))
    
    prompt = f"""
    You are a Cloud Billing Simulator.
    Generate a JSON list of 10-15 realistic cloud billing records for the following project.
    
    Project: {profile.get('name')}
    Budget: {budget} INR per month
    Tech Stack: {tech_stack}
    
    Constraints:
    - Total cost should be roughly around the budget (can be slightly over or under, generate variance).
    - Include services like Compute (EC2/VM), Database (RDS/MongoDB), Storage (S3), Networking, etc.
    - Fields per record: "month" (e.g., "2025-01"), "service", "resource_id", "region", "usage_type", "usage_quantity", "unit", "cost_inr", "desc".
    - Region should be consistent (e.g., "ap-south-1").
    
    Return ONLY the JSON list.
    """
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response_text = query_llm(messages, max_tokens=3000, temperature=0.4)
        
        if response_text:
            billing_data = extract_json_from_text(response_text)
            
            if billing_data and isinstance(billing_data, list):
                return billing_data
            else:
                 print(f"Failed to parse billing JSON. Response snippet: {response_text[:200]}...")
                 return None
        else:
             print(f"LLM returned no response.")
             return None

    except Exception as e:
        print(f"Error during billing generation: {e}")
        return None
