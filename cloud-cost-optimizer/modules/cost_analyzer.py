


def analyze_costs(profile, billing_data):
    """
    Analyzes costs against budget.
    """
    if not profile or not billing_data:
        print("Missing profile or billing data for analysis.")
        return None

    project_name = profile.get('name', 'Unknown Project')
    budget = profile.get('budget_inr_per_month', 0)
    
    # 1. Perform Manual Analysis
    total_cost = 0
    service_costs = {}
    
    for record in billing_data:
        cost = record.get('cost_inr', 0)
        service = record.get('service', 'Other')
        
        total_cost += cost
        service_costs[service] = service_costs.get(service, 0) + cost
        
    budget_variance = total_cost - budget
    is_over_budget = total_cost > budget
    
    # Sort services by cost
    sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
    high_cost_services = {k: v for k, v in sorted_services[:3]} # Top 3
    
    analysis_summary = {
        "total_monthly_cost": total_cost,
        "budget": budget,
        "budget_variance": budget_variance,
        "service_costs": service_costs,
        "high_cost_services": high_cost_services,
        "is_over_budget": is_over_budget
    }
    
    return analysis_summary
