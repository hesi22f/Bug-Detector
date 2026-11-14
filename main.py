"""
Bug Detector - CLI entry point.
Detects bugs in Python code and reports them in English.

Usage:
    python main.py path/to/file.py
    python main.py path/to/project/
    python main.py path/to/project/ --json
    python main.py path/to/file.py --llm
"""

import argparse
import json
import sys
from pathlib import Path

from detector.static_analyzer import analyze_target


def print_report(result: dict) -> None:
    if "error" in result:
        print(f"[ERROR] {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(f"Target        : {result['target']}")
    print(f"Python files  : {result['files_scanned']}")
    print(f"Total issues  : {result['total_issues']}")
    print("-" * 60)

    if result["total_issues"] == 0:
        print("No issues found.")
        return

    by_file: dict[str, list[dict]] = {}
    for issue in result["issues"]:
        by_file.setdefault(issue.get("file") or "<unknown>", []).append(issue)

    for filepath, issues in sorted(by_file.items()):
        print(f"\n{filepath}")
        for issue in sorted(issues, key=lambda x: x.get("line", 0)):
            print(
                f"  Line {issue['line']:>4}, Col {issue['col']:>3}  "
                f"[{issue['code']}]  {issue['message']}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bug Detector - static and optional LLM analysis for Python code."
    )
    parser.add_argument("target", help="File or directory to analyze")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    parser.add_argument("--output", "-o", help="Write report to a file")
    parser.add_argument("--llm", action="store_true", help="Also run LLM analysis on a single file")
    args = parser.parse_args()

    result = analyze_target(args.target)

    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Report written to {args.output}")
        else:
            print(output)
    else:
        print_report(result)
        if args.output:
            text = json.dumps(result, indent=2, ensure_ascii=False)
            Path(args.output).write_text(text, encoding="utf-8")
            print(f"\nReport also written to {args.output}")

    if args.llm:
        from detector.llm_analyzer import analyze_with_llm
        print("\n" + "=" * 60)
        print("LLM ANALYSIS")
        print("=" * 60)
        print(analyze_with_llm(args.target))


if __name__ == "__main__":
    main()