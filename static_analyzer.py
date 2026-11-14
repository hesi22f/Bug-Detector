"""
Static analysis module.
Runs Ruff and Pyflakes on a file or directory and returns English issue reports.
"""

import json
import subprocess
from pathlib import Path

# Directories that must never be scanned (critical for large projects)
SKIP_DIRS = {
    "venv", ".venv", "env", ".env",
    ".git", "__pycache__", "node_modules",
    ".tox", ".eggs", "build", "dist",
    ".mypy_cache", ".pytest_cache", ".ruff_cache",
}

# Ruff rules selected for good signal-to-noise ratio on real projects
RUFF_SELECT = "F,E,W,I,N,UP,B,A,SIM,RET,ARG,C4"
RUFF_IGNORE = "E501,E402,W503"


def should_skip(path: Path) -> bool:
    """Return True if any part of the path is a skip directory or hidden folder."""
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
        # Skip hidden dirs (starting with '.') but keep the file name itself
        if part.startswith(".") and part not in {".", ".."}:
            return True
    return False


def collect_python_files(target: Path) -> list[Path]:
    """Collect all .py files from a file or directory, skipping noise."""
    if target.is_file():
        return [target] if target.suffix == ".py" else []

    files: list[Path] = []
    for path in target.rglob("*.py"):
        if not should_skip(path.relative_to(target)):
            files.append(path)
    return files


def _run_ruff(target: Path) -> list[dict]:
    issues: list[dict] = []
    try:
        result = subprocess.run(
            [
                "ruff", "check", str(target),
                "--output-format=json",
                "--select", RUFF_SELECT,
                "--ignore", RUFF_IGNORE,
                "--no-cache",
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
        data = json.loads(result.stdout or "[]")
        for item in data:
            issues.append({
                "file": item.get("filename", ""),
                "line": item.get("location", {}).get("row", 0),
                "col": item.get("location", {}).get("column", 0),
                "code": item.get("code", "?"),
                "message": item.get("message", ""),
                "source": "ruff",
            })
    except FileNotFoundError:
        issues.append({
            "file": "", "line": 0, "col": 0, "code": "SETUP",
            "message": "Ruff is not installed. Run: pip install ruff",
            "source": "setup",
        })
    except subprocess.TimeoutExpired:
        issues.append({
            "file": str(target), "line": 0, "col": 0, "code": "TIMEOUT",
            "message": "Ruff timed out on this target.",
            "source": "ruff",
        })
    except Exception as exc:
        issues.append({
            "file": str(target), "line": 0, "col": 0, "code": "ERROR",
            "message": f"Ruff error: {exc}",
            "source": "ruff",
        })
    return issues


def _run_pyflakes(target: Path) -> list[dict]:
    issues: list[dict] = []
    try:
        result = subprocess.run(
            ["python", "-m", "pyflakes", str(target)],
            capture_output=True,
            text=True,
            timeout=180,
        )
        for line in result.stdout.strip().splitlines():
            # Format: path:line:col: message
            parts = line.split(":", 3)
            if len(parts) >= 4:
                issues.append({
                    "file": parts[0],
                    "line": int(parts[1]) if parts[1].strip().isdigit() else 0,
                    "col": int(parts[2]) if parts[2].strip().isdigit() else 0,
                    "code": "pyflakes",
                    "message": parts[3].strip(),
                    "source": "pyflakes",
                })
    except FileNotFoundError:
        issues.append({
            "file": "", "line": 0, "col": 0, "code": "SETUP",
            "message": "Pyflakes is not installed. Run: pip install pyflakes",
            "source": "setup",
        })
    except subprocess.TimeoutExpired:
        issues.append({
            "file": str(target), "line": 0, "col": 0, "code": "TIMEOUT",
            "message": "Pyflakes timed out on this target.",
            "source": "pyflakes",
        })
    except Exception as exc:
        issues.append({
            "file": str(target), "line": 0, "col": 0, "code": "ERROR",
            "message": f"Pyflakes error: {exc}",
            "source": "pyflakes",
        })
    return issues


def analyze_target(target_path: str) -> dict:
    """
    Analyze a file or directory.
    Returns a dict with metadata and a list of unique issues.
    """
    target = Path(target_path).resolve()

    if not target.exists():
        return {"error": f"Path not found: {target}"}

    files = collect_python_files(target)
    if not files:
        return {"error": f"No Python files found in: {target}"}

    raw_issues = _run_ruff(target) + _run_pyflakes(target)

    # De-duplicate on (file, line, message)
    seen = set()
    unique: list[dict] = []
    for issue in raw_issues:
        key = (issue.get("file"), issue.get("line"), issue.get("message"))
        if key not in seen:
            seen.add(key)
            unique.append(issue)

    # Sort by file then line
    unique.sort(key=lambda x: (x.get("file", ""), x.get("line", 0)))

    return {
        "target": str(target),
        "files_scanned": len(files),
        "issues": unique,
        "total_issues": len(unique),
    }