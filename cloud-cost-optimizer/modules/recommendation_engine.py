from .llm_client import query_llm, extract_json_from_text
import json

def generate_recommendations(profile, analysis_summary):
    """
    Generates cost optimization recommendations using LLM based on profile and cost analysis.
    """
    if not profile or not analysis_summary:
        print("Missing profile or analysis summary for recommendations.")
        return []

    project_name = profile.get('name', 'Unknown Project')
    
    total_cost = analysis_summary.get('total_monthly_cost', 0)
    budget = analysis_summary.get('budget', 0)
    budget_variance = analysis_summary.get('budget_variance', 0)
    service_costs = analysis_summary.get('service_costs', {})

    prompt = f"""
    You are a Cloud FinOps Expert.
    Based on the following project profile and cost analysis, provide 6-10 cost optimization recommendations.
    
    Project: {project_name}
    Tech Stack: {json.dumps(profile.get('tech_stack', {}))}
    Non-Functional Reqs: {json.dumps(profile.get('non_functional_requirements', []))}
    
    Cost Analysis:
    Total Cost: {total_cost} INR
    Budget: {budget} INR
    Variance: {budget_variance} INR
    Service Costs: {json.dumps(service_costs)}
    
    Task:
    Generate a JSON list of recommendations. 
    Each recommendation must include:
    - title
    - service (target service)
    - current_cost (approx from analysis)
    - potential_savings (estimate)
    - recommendation_type (e.g., "open_source", "free_tier", "right_sizing", "alternative_provider")
    - description
    - implementation_effort ("low", "medium", "high")
    - risk_level ("low", "medium", "high")
    - steps (list of strings)
    - cloud_providers (list of applicable providers)
    
    Focus on multi-cloud suggestions (AWS, Azure, GCP, DigitalOcean) and open-source alternatives.
    
    Return ONLY the list of recommendations as a valid JSON array.
    """
    
    messages = [{"role": "user", "content": prompt}]
    
    recommendations = []
    try:
        response_text = query_llm(messages, max_tokens=2000, temperature=0.3)
        
        if response_text:
            extracted = extract_json_from_text(response_text)
            if isinstance(extracted, list):
                recommendations = extracted
            elif isinstance(extracted, dict) and 'recommendations' in extracted:
                recommendations = extracted['recommendations']
            else:
                 print(f"Failed to parse recommendations JSON. Raw text might be useful for debugging.")
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        
    return recommendations
