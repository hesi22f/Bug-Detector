# 🐞 Bug Detector

> **A Python CLI tool that detects bugs in your code using Ruff, Pyflakes, and optional LLM analysis — with clear English reports for single files or entire projects.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/linter-Ruff-red.svg)](https://github.com/astral-sh/ruff)
[![Pyflakes](https://img.shields.io/badge/linter-Pyflakes-green.svg)](https://github.com/PyCQA/pyflakes)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Why Bug Detector?](#-why-bug-detector)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Example Output](#-example-output)
- [LLM Analysis](#-llm-analysis)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Use Cases](#-use-cases)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🔍 Overview

**Bug Detector** is a lightweight, fast, and practical command-line tool that finds bugs in Python code. It combines two well-established static analyzers — **Ruff** and **Pyflakes** — and optionally augments them with an **LLM-based analyzer** for logic bugs and security issues that traditional linters cannot catch.

The tool works on **small scripts** and **large multi-file projects**, with recursive scanning, smart directory skipping, and JSON output suitable for CI/CD pipelines.

All reports are printed in **English**, so they integrate naturally with GitHub, GitLab, and other developer tooling.

---

## 💡 Why Bug Detector?

Most Python linters are excellent at catching stylistic issues and simple mistakes, but they are:

- **Too noisy** — thousands of style warnings hide the real bugs.
- **Not beginner-friendly** — messages assume familiarity with rule codes.
- **Limited to syntax and static patterns** — they cannot reason about logic or security context.

**Bug Detector** solves this by:

1. **Focused static analysis** — running Ruff with a curated set of high-signal rules plus Pyflakes for undefined names and unused imports.
2. **Smart scoping** — skipping `venv`, `.git`, `node_modules`, and cache folders so large projects stay fast.
3. **Optional AI layer** — sending code to an LLM to reason about logic, edge cases, and security issues.
4. **English reports** — no translation needed, ready for international teams and CI systems.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔎 **Static analysis** | Runs **Ruff** and **Pyflakes** with curated rules |
| 🌍 **English reports** | Every issue includes file, line, column, rule code, and message |
| 📁 **File or directory** | Analyze a single file or recursively scan a whole project |
| 🚫 **Smart skipping** | Ignores `venv`, `.git`, `__pycache__`, `node_modules`, `build`, `dist`, caches, and hidden folders |
| 🤖 **Optional LLM analysis** | Detects logic bugs, security issues, and edge cases with OpenAI models |
| 📊 **JSON output** | Machine-readable output for CI/CD, dashboards, or other tools |
| 💾 **Save to file** | Write the report to disk with `-o report.json` |
| ⚡ **Fast** | Powered by Ruff, one of the fastest Python linters available |
| 🧩 **Extensible** | Clean module structure — easy to plug in new analyzers |
| 🛡️ **Safe by default** | No network calls unless `--llm` is explicitly used |

---

## ⚙️ How It Works

```
                ┌───────────────────────────────┐
                │        User runs CLI          │
                │  python main.py path/ [--llm] │
                └───────────────┬───────────────┘
                                │
                ┌───────────────▼───────────────┐
                │  collect_python_files(target) │
                │  (skips venv, .git, caches…)  │
                └───────────────┬───────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────▼───────┐       ┌───────▼───────┐       ┌───────▼────────┐
│  Ruff runner  │       │ Pyflakes run. │       │  LLM analyzer  │
│  (JSON out)   │       │  (text out)   │       │  (optional)    │
└───────┬───────┘       └───────┬───────┘       └───────┬────────┘
        │                       │                       │
        └───────────┬───────────┘                       │
                    │                                   │
        ┌───────────▼────────────┐            ┌─────────▼──────────┐
        │  De-duplication & sort │            │  English narrative │
        └───────────┬────────────┘            └─────────┬──────────┘
                    │                                   │
        ┌───────────▼────────────┐                      │
        │  Text / JSON report    │◄─────────────────────┘
        └───────────┬────────────┘
                    │
        ┌───────────▼────────────┐
        │   Console or file      │
        └────────────────────────┘
```

---

## 🧰 Requirements

- **Python** 3.9 or newer
- **Ruff** ≥ 0.6.0
- **Pyflakes** ≥ 3.2.0
- **OpenAI** ≥ 1.0.0 *(only for `--llm`)*

---

## 🚀 Installation

### 1) Clone the repository

```bash
git clone https://github.com/<your-username>/bug-detector.git
cd bug-detector
```

### 2) Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Verify installation

```bash
python main.py --help
```

---

## 🕹️ Usage

### Analyze a single file

```bash
python main.py path/to/file.py
```

### Analyze an entire project

```bash
python main.py path/to/project/
```

### Output as JSON

```bash
python main.py path/to/project/ --json
```

### Save report to a file

```bash
python main.py path/to/project/ --json -o report.json
```

### Run LLM analysis as well (single file)

```bash
export OPENAI_API_KEY=sk-...
python main.py path/to/file.py --llm
```

### Command-line options

| Option | Description |
|---|---|
| `target` | File or directory to analyze *(required)* |
| `--json` | Print report as JSON |
| `--output`, `-o` | Write report to the given file |
| `--llm` | Also run LLM analysis (single file, requires `OPENAI_API_KEY`) |
| `--help` | Show help message |

---

## 📸 Example Output

```text
$ python main.py tests/sample_buggy.py

Target        : /home/user/bug-detector/tests/sample_buggy.py
Python files  : 1
Total issues  : 4
------------------------------------------------------------

/home/user/bug-detector/tests/sample_buggy.py
  Line    1, Col   1  [F401]  `os` imported but unused
  Line    2, Col   1  [F401]  `sys` imported but unused
  Line    9, Col  12  [F821]  Undefined name `undefined_discount`
  Line   19, Col   1  [F841]  Local variable `unused_function` is assigned to but never used
```

JSON output:

```json
{
  "target": "/home/user/bug-detector/tests/sample_buggy.py",
  "files_scanned": 1,
  "total_issues": 4,
  "issues": [
    {
      "file": ".../sample_buggy.py",
      "line": 1,
      "col": 1,
      "code": "F401",
      "message": "`os` imported but unused",
      "source": "ruff"
    }
  ]
}
```

---

## 🤖 LLM Analysis

When `--llm` is provided, the tool sends the file content to an OpenAI model and asks for a structured English review of **logic bugs, security issues, unhandled edge cases, and serious performance problems** — ignoring style and naming.

Example prompt output:

```text
Line 15: Division by zero
Reason: `a / b` will raise ZeroDivisionError when `b == 0`.
Fix: Add `if b == 0: raise ValueError("b must be non-zero")` or return a default.

Line 9: Undefined variable
Reason: `undefined_discount` is referenced but never defined.
Fix: Define `undefined_discount = 0` or remove it from the expression.
```

> **Note:** The LLM layer is **opt-in**. Without `--llm`, the tool performs **only local static analysis** and makes **no network calls**.

Environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | *(unset)* | Required for `--llm` |
| `BUG_DETECTOR_MODEL` | `gpt-4o-mini` | Override the model used |

---

## 🗂️ Project Structure

```text
bug-detector/
├── detector/
│   ├── __init__.py
│   ├── static_analyzer.py    # Ruff + Pyflakes integration
│   └── llm_analyzer.py       # Optional OpenAI-based analysis
├── tests/
│   └── sample_buggy.py       # Sample file with intentional bugs
├── main.py                   # CLI entry point
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

| File | Responsibility |
|---|---|
| `main.py` | CLI parsing, orchestration, report rendering |
| `detector/static_analyzer.py` | File collection, skipping logic, Ruff/Pyflakes runners, de-duplication |
| `detector/llm_analyzer.py` | Prompt construction, OpenAI call, English response formatting |
| `tests/sample_buggy.py` | Reproducible example for manual and CI tests |

---

## 🔧 Configuration

The tool is intentionally configurable via code constants, so you can tailor it to your team:

- **`SKIP_DIRS`** in `static_analyzer.py` — directories never scanned.
- **`RUFF_SELECT`** — which Ruff rule families are enabled (`F`, `E`, `W`, `I`, `N`, `UP`, `B`, `A`, `SIM`, `RET`, `ARG`, `C4`).
- **`RUFF_IGNORE`** — rules you may want to silence (`E501`, `E402`, `W503`).
- **`DEFAULT_MODEL`** — OpenAI model used by `llm_analyzer.py`.
- **`max_chars`** in `_read_file` — truncation limit for large files sent to the LLM.

---

## 🎯 Use Cases

- **Pre-commit checks** — run on staged files before committing.
- **CI/CD pipelines** — use `--json` output to fail builds on real bugs.
- **Code review assistance** — attach `report.json` to PRs.
- **Learning tool** — English messages help beginners understand why something is a bug.
- **Large monorepos** — recursive scan with smart skipping keeps it fast.
- **AI-assisted debugging** — `--llm` surfaces bugs static analysis misses.

---

## 🗺️ Roadmap

- [ ] **GitHub Action** for automatic PR comments
- [ ] **Multi-language support** (JavaScript, TypeScript, C++)
- [ ] **SARIF export** for GitHub Code Scanning
- [ ] **Custom rule configuration** via `pyproject.toml`
- [ ] **Streamlit web UI** for interactive analysis
- [ ] **Local LLM support** via Ollama
- [ ] **Diff mode** — analyze only files changed since last commit

---

## 🤝 Contributing

Contributions are welcome and appreciated!

1. **Fork** the repository.
2. **Create a branch**: `git checkout -b feature/my-feature`.
3. **Commit your changes**: `git commit -m "Add my feature"`.
4. **Push**: `git push origin feature/my-feature`.
5. **Open a Pull Request**.

Please keep code style consistent with existing files and add tests for new behavior.

### Reporting bugs

Open an issue with:
- The command you ran
- The file or project shape (if shareable)
- The output you received
- The output you expected

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Ruff](https://github.com/astral-sh/ruff) — blazing-fast Python linter by Astral
- [Pyflakes](https://github.com/PyCQA/pyflakes) — lightweight logic checker
- [OpenAI Python SDK](https://github.com/openai/openai-python) — LLM integration
- The Python community for building the tools that make projects like this possible

---

> **Bug Detector** — *Find real bugs, get clear answers, ship better Python.* 🐍✨
