#!/usr/bin/env python3
"""Convert Gradle JUnit XML reports into structured JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


def text(element: ET.Element | None) -> str:
    return "".join(element.itertext()).strip() if element is not None else ""


def classify_failure(problem_type: str | None, message: str | None, details: str) -> str:
    value = " ".join(filter(None, (problem_type, message, details))).lower()
    if any(token in value for token in ("assert", "expected:", "expected <", "but was:")):
        return "assertion"
    if any(token in value for token in ("timeout", "timed out", "deadline exceeded")):
        return "timeout"
    if any(token in value for token in ("connection refused", "connectexception", "unknownhost")):
        return "external_dependency"
    if any(token in value for token in ("compilation", "unresolved reference", "cannot find symbol")):
        return "compilation"
    return "exception"


def first_source_location(details: str) -> str | None:
    for line in details.splitlines():
        if re.search(r"\bat .+\([^)]+:\d+\)", line):
            return line.strip()
    return None


def print_agent_summary(result: dict[str, Any]) -> None:
    summary = result["summary"]
    status = result["status"].upper()
    print(
        f"{status}: {summary['total']} total, "
        f"{summary['passed']} passed, {summary['failed'] + summary['errored']} failed, "
        f"{summary['skipped']} skipped"
    )
    for failed_test in result["failed_tests"]:
        message = failed_test["message"] or failed_test["type"] or "failure"
        print(
            f"- {failed_test['id']} [{failed_test['diagnostic_category']}]: "
            f"{message}"
        )
        location = first_source_location(failed_test["details"])
        if location:
            print(f"  {location}")
    if result["status"] != "passed":
        if result.get("report"):
            print(f"Report: {result['report']}")
        if result.get("raw_log"):
            print(f"Details: {result['raw_log']}")


def parse_results(results_dir: Path, task: str, raw_log: Path | None) -> dict[str, Any]:
    summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errored": 0}
    failed_tests: list[dict[str, Any]] = []
    report_files = sorted(results_dir.rglob("*.xml")) if results_dir.exists() else []

    for report_file in report_files:
        try:
            root = ET.parse(report_file).getroot()
        except ET.ParseError as error:
            print(f"Warning: unable to parse {report_file}: {error}", file=sys.stderr)
            continue

        testcases = [root] if root.tag == "testcase" else root.iter("testcase")
        for testcase in testcases:
            name = testcase.get("name", "unknown")
            class_name = testcase.get("classname", "unknown")
            identifier = f"{class_name}#{name}"
            failure = testcase.find("failure")
            error = testcase.find("error")
            skipped = testcase.find("skipped") is not None
            system_out = text(testcase.find("system-out"))
            system_err = text(testcase.find("system-err"))

            summary["total"] += 1
            if skipped:
                summary["skipped"] += 1
                continue

            if failure is not None or error is not None:
                summary["failed" if failure is not None else "errored"] += 1
                problem = failure if failure is not None else error
                message = problem.get("message") if problem is not None else None
                problem_type = problem.get("type") if problem is not None else None
                details = text(problem)
                failed_tests.append(
                    {
                        "id": identifier,
                        "name": name,
                        "class_name": class_name,
                        "duration_seconds": testcase.get("time"),
                        "kind": "failure" if failure is not None else "error",
                        "message": message,
                        "type": problem_type,
                        "diagnostic_category": classify_failure(problem_type, message, details),
                        "details": details,
                        "logs": {
                            "system_out": system_out,
                            "system_err": system_err,
                        },
                        "report_file": str(report_file),
                    }
                )
            else:
                summary["passed"] += 1

    status = "failed" if summary["failed"] or summary["errored"] else (
        "passed" if summary["total"] else "no-results"
    )
    result: dict[str, Any] = {
        "status": status,
        "task": task,
        "results_directory": str(results_dir),
        "summary": summary,
        "failed_tests": failed_tests,
    }
    if raw_log is not None:
        result["raw_log"] = str(raw_log)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--task", default="test")
    parser.add_argument("--raw-log", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--agent-summary",
        action="store_true",
        help="Print a concise agent-oriented summary instead of JSON",
    )
    args = parser.parse_args()

    result = parse_results(args.results_dir, args.task, args.raw_log)
    if args.output:
        result["report"] = str(args.output)
        args.output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    if args.agent_summary:
        print_agent_summary(result)
    else:
        print(encoded)
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
