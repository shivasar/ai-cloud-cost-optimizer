# Cloud Cost Optimizer

**Overview**

- **Purpose:** Analyze cloud billing data, extract a project profile, run cost analysis, and produce actionable recommendations and a report.
- **Outcome:** Generates `cost_optimization_report.json` with findings and recommendations.

**Project Flow**

- **Orchestrator:** The entrypoint is [main.py](main.py) which ties the modules together and writes the final report.
- **Profile extraction:** [modules/profile_extractor.py](modules/profile_extractor.py) reads `project_profile.json` to build a project context.
- **Billing input:** Billing data comes from `mock_billing.json` or a real billing export; [modules/billing_generator.py](modules/billing_generator.py) provides sample data for testing.
- **Cost analysis:** [modules/cost_analyzer.py](modules/cost_analyzer.py) processes billing records and computes cost breakdowns and trends.
- **Recommendations:** [modules/recommendation_engine.py](modules/recommendation_engine.py) creates optimization suggestions based on analysis results.
- **LLM support:** [modules/llm_client.py](modules/llm_client.py) (optional) formats prompts and calls an LLM to produce human-friendly explanations.

Example high-level flow:

1. `profile_extractor` loads the project profile.
2. `billing_generator` supplies billing records (or real export is loaded).
3. `cost_analyzer` aggregates costs and identifies hotspots.
4. `recommendation_engine` maps hotspots to actionable changes.
5. `main.py` orchestrates calls and writes `cost_optimization_report.json`.

**How to run locally (Windows)**

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the tool (uses `mock_billing.json` and `project_profile.json` by default):

```powershell
python main.py
```

4. Quick test run (lightweight):

```powershell
python test.py
```

**Important files**

- **Entrypoint:** [main.py](main.py)
- **Sample billing:** [mock_billing.json](mock_billing.json)
- **Project profile:** [project_profile.json](project_profile.json)
- **Report output:** `cost_optimization_report.json` (created after run)
- **Modules:** See the `modules/` folder for `billing_generator.py`, `cost_analyzer.py`, `profile_extractor.py`, `recommendation_engine.py`, and `llm_client.py`.

**Notes & troubleshooting**

- If you want to use real billing exports, replace `mock_billing.json` or modify `main.py` to point at your file.
- If LLM calls are enabled, ensure API keys/config are set in environment variables or the place expected by `modules/llm_client.py`.
- For permission or environment errors, confirm your Python version matches `requirements.txt` and the virtual environment is activated.

