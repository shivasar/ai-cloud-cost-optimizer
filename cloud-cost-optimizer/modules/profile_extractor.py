from .llm_client import query_llm, extract_json_from_text
def extract_project_profile(description):
    prompt = f"""
    Analyze this project description and return a JSON object with:
    - name: Project Name
    - budget_inr_per_month: Estimated monthly budget in INR (int)
    - tech_stack: {{frontend, backend, database, etc.}}
    
    Description: "{description}"
    
    Return ONLY JSON.
    """
    
    response = query_llm([{"role": "user", "content": prompt}], max_tokens=500)
    return extract_json_from_text(response)