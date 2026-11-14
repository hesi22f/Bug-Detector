# Bug-Detector
Find real bugs in your Python code — static analysis meets AI, with clean English reports built for projects of any size.
# Bug Detector

A simple Python tool that detects bugs in Python code and reports them in English.
Works on single files or entire projects.

## Features

- Static analysis with **Ruff** and **Pyflakes** (English messages, line/column)
- Recursive scan of large projects
- Skips `venv`, `.git`, `__pycache__`, `node_modules`, etc.
- Optional **LLM analysis** for logic bugs and security issues (OpenAI)
- JSON output for CI/CD integration

## Install

```bash
git clone https://github.com/<your-username>/bug-detector.git
cd bug-detector
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
