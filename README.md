# Task AI Tester

**Task AI Tester** is a lightweight FastAPI-based project demonstrating AI-driven API testing automation.  
It consists of two FastAPI services (Task API and AI Test Agent) and a demo script that runs the full end-to-end process automatically.

---

## Folder Structure

```
task-ai/
├── agent/
│   └── ai_test_agent.py        # AI Test Agent – generates, executes, and analyzes test cases via OpenAI API
├── api/
│   └── app.py                  # Simple FastAPI task management API (CRUD for tasks)
├── tests/
│   └── test_integration.py     # Integration tests (optional, for pytest)
├── demo.py                     # One-click demo script that runs the entire flow
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── report.md                   # Generated QA report (AI summary)
└── pytest.ini                  # Pytest configuration
```

---

## Requirements

- **Python 3.11+** (tested on 3.12)
- **pip** package manager
- **OpenAI API key** (active billing required)
- Works on Windows, macOS, or Linux

Default ports:
- **5000** → Task API  
- **5001** → AI Test Agent

---

## Installation and Setup

### 1. Clone and navigate to the project folder

```bash
git clone https://github.com/milanmmaximovic/ai-agent-task.git
cd ai-agent-task
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scriptsctivate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set the OpenAI API key

You must have an active OpenAI key from the [OpenAI Platform](https://platform.openai.com/).

```powershell
$env:OPENAI_API_KEY = "your-secret-key"
```

or on macOS/Linux:

```bash
export OPENAI_API_KEY="your-secret-key"
```

---

## Running Locally

### 1. Start the Task API (port 5000)

```bash
uvicorn api.app:app --reload --port 5000
```

### 2. Start the AI Test Agent (port 5001)

```bash
uvicorn agent.ai_test_agent:app --reload --port 5001
```

### 3. Run the one-click demo

```bash
python demo.py
```

This script will:
1. Verify both services are up  
2. Fetch the OpenAPI spec  
3. Generate realistic test scenarios using the AI model  
4. Execute all generated API tests  
5. Analyze results and produce a Markdown QA report (`report.md`)

---

## Example Output

After a successful run, you’ll see console output similar to:

```
AI Test Agent Starting...
Generated 14 test scenarios using AI
Executed 14 tests in 22.3 seconds
Results: 12 passed, 2 failed
Executive Summary: saved to report.md
```

And a `report.md` file will contain a detailed AI-written analysis report in Markdown format.

---

## Development Notes

- Both services can be customized or extended for different APIs by modifying:
  - `/api/app.py` for business logic (your own API under test)
  - `/agent/ai_test_agent.py` for test generation logic or OpenAI prompts
- `demo.py` provides a single command demonstration flow.
- Integration tests can be added under `/tests`.

---

## Deactivate Environment

When finished working, deactivate your Python virtual environment:

```bash
deactivate
```

---

## License

This project is provided for educational and testing purposes.
