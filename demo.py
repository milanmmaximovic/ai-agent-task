# task_ai_tester/demo.py
import requests, time, sys, json, os
from pathlib import Path

AGENT_URL = os.getenv("AGENT_URL", "http://127.0.0.1:5001")
API_URL   = os.getenv("API_URL",   "http://127.0.0.1:5000")
REPORT_PATH = Path("./report.md")

def main():
    print("AI Test Agent Starting...")

    payload = {"base_url": API_URL}
    start_time = time.time()

    try:
        response = requests.post(f"{AGENT_URL}/run", json=payload, timeout=180)
    except Exception as e:
        print(f"Request to AI agent failed: {e}")
        sys.exit(1)

    if response.status_code >= 400:
        print(f"Agent returned HTTP {response.status_code}")
        print(response.text[:800])
        sys.exit(1)

    data = response.json()

    # Extract scenarios
    scenarios = data.get("scenarios", []) or []
    print(f"Generated {len(scenarios)} test scenarios using AI")

    # Extract results and compute stats
    execution = data.get("execution", {}) or {}
    results = execution.get("results", []) or []

    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    failed = total - passed
    duration = time.time() - start_time

    print(f"Executed {total} tests in {duration:.1f} seconds")
    print(f"Results: {passed} passed, {failed} failed")

    # AI analysis
    report = data.get("report", {}) or {}
    summary_points = report.get("summary", []) or []
    if summary_points:
        print("AI Analysis / Recommendations:")
        for point in summary_points[:8]:
            print(f"- {point}")

    # Save Markdown report
    report_md = report.get("report_md", "# Report not available")
    try:
        REPORT_PATH.write_text(report_md, encoding="utf-8")
        print(f"Executive Summary saved to {REPORT_PATH.resolve()}")
    except Exception as e:
        print(f"Could not save report.md: {e}")

    if failed > 0:
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
