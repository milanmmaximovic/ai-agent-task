
import pytest
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")
AGENT_URL = os.getenv("AGENT_URL", "http://127.0.0.1:5001")

@pytest.mark.smoke
def test_health_endpoints():
    r1 = requests.get(f"{API_URL}/health")
    r2 = requests.get(f"{AGENT_URL}/health")
    assert r1.status_code == 200
    assert r1.json() == {"status": "ok"}
    assert r2.status_code == 200
    assert r2.json() == {"status": "ok"}

@pytest.mark.functional
def test_ai_agent_end_to_end():
    payload = {"base_url": API_URL}
    resp = requests.post(f"{AGENT_URL}/run", json=payload, timeout=180)
    assert resp.status_code == 200, f"AI agent run failed: {resp.text[:500]}"
    data = resp.json()
    assert "analysis" in data
    assert "scenarios" in data
    assert "execution" in data
    assert "report" in data
