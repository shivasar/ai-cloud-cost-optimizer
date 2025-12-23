import sys
import json
from rich.console import Console
from rich.prompt import Prompt
from modules.profile_extractor import extract_project_profile

console = Console()
def main():
    console.print("[bold blue]Cloud Cost Optimizer[/bold blue]")
    
    # 1. Get Input
    desc = Prompt.ask("Describe your project")
    
    # 2. Extract Profile
    with console.status("Analyzing..."):
        profile = extract_project_profile(desc)
    console.print(f"Project Identified: [green]{profile['name']}[/green]")
    
if __name__ == "__main__":
    main()