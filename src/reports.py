"""Write the assignment deliverables: case study, solution guide, and resources."""
from __future__ import annotations

from pathlib import Path
import json

from .config import ROOT


def _md_value(value) -> str:
    if isinstance(value, (dict, list)):
        return "```json\n" + json.dumps(value, indent=2, default=str) + "\n```"
    return str(value)


def write_docs(findings: dict) -> list[Path]:
    docs = ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    dictionary = findings.get("data_dictionary") or {}
    dict_rows = "\n".join(f"| `{k}` | {v} |" for k, v in dictionary.items())
    case = f"""# Case study — {findings['title']}

## Problem statement
{findings['problem_statement']}

## Overview
{findings['overview']}

## Stakeholders
- Internal: {', '.join(findings['stakeholders']['internal'])}
- External: {', '.join(findings['stakeholders']['external'])}

## Data dictionary
| Column | Description |
| --- | --- |
{dict_rows}

## Assignment questions
The brief's basic, medium, and advanced questions are answered in `docs/SOLUTION_GUIDE.md` and `outputs/{findings['slug']}/findings.json`.
"""
    qa_parts = ["# Solution guide\n", f"Answers for **{findings['title']}**.\n"]
    for level, rows in findings.get("qa", {}).items():
        qa_parts.append(f"\n## {level.title()}-level questions\n")
        for i, row in enumerate(rows, 1):
            qa_parts.append(f"### {i}. {row['q']}\n")
            if row.get("how_it_helps"):
                qa_parts.append(f"- How it helps: {row['how_it_helps']}\n")
            if row.get("business_impact"):
                qa_parts.append(f"- Business impact: {row['business_impact']}\n")
            qa_parts.append(_md_value(row["a"]) + "\n")
    resources = findings.get("additional_resources") or []
    extra = findings.get("resume_snippet")
    res = "# Additional resources\n\n" + "\n".join(f"- {r}" for r in resources) + "\n"
    if extra:
        res += "\n## Resume snippet\n\n" + extra + "\n"

    paths = [
        docs / "CASE_STUDY.md",
        docs / "SOLUTION_GUIDE.md",
        docs / "ADDITIONAL_RESOURCES.md",
    ]
    paths[0].write_text(case, encoding="utf-8")
    paths[1].write_text("".join(qa_parts), encoding="utf-8")
    paths[2].write_text(res, encoding="utf-8")
    return paths
