# task_ai_tester/demo.py
import requests, time, sys, json, os
from pathlib import Path

AGENT_URL = os.getenv("AGENT_URL", "http://127.0.0.1:5001")
API_URL   = os.getenv("API_URL",   "http://127.0.0.1:5000")
REPORT_PATH = Path("./report.md")

def main():
    print("🤖 AI Test Agent Starting...")
    # quick health checks (optional, but friendly)
    try:
        requests.get(f"{API_URL}/health", timeout=5)
        requests.get(f"{AGENT_URL}/health", timeout=5)
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("   Make sure FastAPI runs on 5000 and AI agent on 5001.")
        sys.exit(1)

    payload = {"base_url": API_URL}
    t0 = time.time()
    try:
        resp = requests.post(f"{AGENT_URL}/run", json=payload, timeout=180)
    except Exception as e:
        print(f"❌ Request to AI agent failed: {e}")
        sys.exit(1)

    if resp.status_code >= 400:
        print(f"❌ Agent returned HTTP {resp.status_code}")
        print(resp.text[:1000])
        sys.exit(1)

    data = resp.json()

    # scenarios
    scenarios = data.get("scenarios", [])
    print(f"✅ Generated {len(scenarios)} test scenarios using AI")

    # execution summary
    execution = data.get("execution", {})
    summary = execution.get("summary", {}) or {}
    total   = summary.get("total", 0)
    passed  = summary.get("passed", 0)
    failed  = summary.get("failed", 0)
    took_s  = time.time() - t0

    print(f"✅ Executed {total} tests in {took_s:.1f} seconds")
    print(f"📊 Results: {passed} passed, {failed} failed")

    # AI analysis
    report = data.get("report", {}) or {}
    bullets = report.get("summary", []) or []
    if bullets:
        print("🧠 AI Analysis / Recommendations:")
        for b in bullets[:8]:
            print(f"- {b}")

    # Save markdown report
    report_md = report.get("report_md", "# Report not available")
    try:
        REPORT_PATH.write_text(report_md, encoding="utf-8")
        print(f"📝 Executive Summary: saved to {REPORT_PATH.resolve()}")
    except Exception as e:
        print(f"⚠️ Could not save report.md: {e}")

    # Done
    if failed > 0:
        sys.exit(2)  # non-zero exit if there are failures (optional)
    sys.exit(0)

if __name__ == "__main__":
    main()
