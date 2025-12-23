import os
import sys
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

# Ensure modules structure is accessible
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.profile_extractor import extract_project_profile
from modules.billing_generator import generate_synthetic_billing
from modules.cost_analyzer import analyze_costs
from modules.recommendation_engine import generate_recommendations

console = Console()

DESCRIPTION_FILE = "project_description.txt"
PROFILE_FILE = "project_profile.json"
BILLING_FILE = "mock_billing.json"
REPORT_FILE = "cost_optimization_report.json"

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    console.print(f"[green]Saved {filename}[/green]")

def load_json(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def enter_description_flow():
    console.print(Panel("[bold blue]Enter Project Description[/bold blue]"))
    console.print("Type your description below (press Enter twice to finish):")
    
    # Simple multi-line input simulation
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    
    description = "\n".join(lines)
    if not description.strip():
        console.print("[red]Description cannot be empty.[/red]")
        return

    with open(DESCRIPTION_FILE, 'w', encoding='utf-8') as f:
        f.write(description)
    console.print(f"[green]Saved description to {DESCRIPTION_FILE}[/green]")
    
    with console.status("[bold green]Extracting Profile...[/bold green]"):
        profile = extract_project_profile(description)
    
    if profile:
        save_json(PROFILE_FILE, profile)
        console.print(Panel(json.dumps(profile, indent=2), title="Extracted Profile"))
    else:
        console.print("[red]Failed to extract profile. Please check your API token or description.[/red]")

def run_analysis_flow():
    profile = load_json(PROFILE_FILE)
    if not profile:
        console.print("[red]No project profile found. Please enter a description first.[/red]")
        return

    with console.status("[bold green]Generating Synthetic Billing...[/bold green]"):
        billing_data = generate_synthetic_billing(profile)
    
    if billing_data:
        save_json(BILLING_FILE, billing_data)
        
        with console.status("[bold green]Analyzing Costs & Generating Recommendations...[/bold green]"):
            analysis = analyze_costs(profile, billing_data)
            recommendations = generate_recommendations(profile, analysis)

            report = {
                "project_name": profile.get('name', 'Unknown Project'),
                "analysis": analysis,
                "recommendations": recommendations,
                "summary": {
                    "total_potential_savings": sum([r.get('potential_savings', 0) for r in recommendations]),
                    "recommendations_count": len(recommendations)
                }
            }
        
        if report:
            save_json(REPORT_FILE, report)
            console.print("[bold green]Analysis Complete![/bold green]")
            display_summary(report)
        else:
            console.print("[red]Failed to generate report.[/red]")
    else:
         console.print("[red]Failed to generate billing data.[/red]")

def display_summary(report):
    if not report:
        report = load_json(REPORT_FILE)
        if not report:
            console.print("[red]No report found.[/red]")
            return

    analysis = report.get('analysis', {})
    console.print(Panel(f"Total Cost: {analysis.get('total_monthly_cost')} INR\n"
                        f"Budget: {analysis.get('budget')} INR\n"
                        f"Variance: {analysis.get('budget_variance')} INR", 
                        title="Cost Summary", style="bold"))
    
    recs = report.get('recommendations', [])
    table = Table(title="Recommendations")
    table.add_column("Title", style="cyan")
    table.add_column("Savings", style="green")
    table.add_column("Type", style="magenta")
    
    for r in recs:
        table.add_row(r.get('title'), str(r.get('potential_savings')), r.get('recommendation_type'))
        
    console.print(table)

def main_menu():
    while True:
        console.print("\n[bold]Cloud Cost Optimizer CLI[/bold]")
        console.print("1. Enter New Project Description")
        console.print("2. Run Complete Cost Analysis")
        console.print("3. View Recommendations")
        console.print("4. Exit")
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            enter_description_flow()
        elif choice == "2":
            run_analysis_flow()
        elif choice == "3":
            display_summary(None)
        elif choice == "4":
            console.print("Goodbye!")
            break

if __name__ == "__main__":
    main_menu()
