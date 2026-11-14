"""
Optional LLM-based analyzer.
Sends code to an LLM and asks for an English explanation of real bugs
that static analysis cannot detect (logic errors, security issues, design flaws).
"""

import os
from pathlib import Path

DEFAULT_MODEL = os.getenv("BUG_DETECTOR_MODEL", "gpt-4o-mini")


def _read_file(path: Path, max_chars: int = 12000) -> str:
    """Read a file, truncating huge files to keep the prompt reasonable."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if len(text) > max_chars:
        text = text[:max_chars] + "\n# ... [truncated] ..."
    return text


def analyze_with_llm(target_path: str) -> str:
    """
    Analyze a single Python file with an LLM.
    Returns an English report as a string.
    """
    try:
        from openai import OpenAI
    except ImportError:
        return "The `openai` package is not installed. Run: pip install openai"

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Environment variable OPENAI_API_KEY is not set."

    target = Path(target_path).resolve()
    if not target.is_file():
        return f"LLM analysis currently supports single files only. Got: {target}"

    code = _read_file(target)

    client = OpenAI(api_key=api_key)
    prompt = f"""You are a senior Python code reviewer.
Analyze the following code and report ONLY real, important issues:
- logic bugs
- security vulnerabilities
- unhandled edge cases
- performance problems with real impact

Ignore style, naming, and formatting.
For each issue, respond in this format:

Line <number>: <short title>
Reason: <why it is a bug>
Fix: <suggestion>

If no real issues are found, reply: "No significant issues found."

Code from file: {target.name}
```python
{code}
```"""

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content or "(empty response)"
    except Exception as exc:
        return f"LLM request failed: {exc}"