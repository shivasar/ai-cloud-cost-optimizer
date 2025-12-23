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

console = Console()

DESCRIPTION_FILE = "project_description.txt"
PROFILE_FILE = "project_profile.json"


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
        
            break

if __name__ == "__main__":
    main_menu()
