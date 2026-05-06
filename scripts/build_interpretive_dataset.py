#!/usr/bin/env python3
"""Build an interpretive modeling dataset with grouped categories."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


TRANSFER_GOALS = {
    "AA Degree w/Transfer Bach.",
    "Bachelor's Degree or higher",
    "4 yr college student meet 4 yr",
}
DEGREE_GOALS = {"AA Degree w/out Transfer"}
CAREER_ED_GOALS = {"Certificate Only", "Two Yr. Vocational Degree"}


def group_residency(value: str) -> str:
    if value == "California Resident":
        return "California Resident"
    if value in {"Foreign", "Non-Resident-Out of state"}:
        return "Nonresident/Foreign"
    return "AB540/Exempt/Other"


def group_ethnicity(value: str) -> str:
    if value in {"Hispanic", "White", "Asian", "Black"}:
        return value
    return "Other/Multiple/Unknown"


def group_gender(value: str) -> str:
    if value in {"F", "M"}:
        return value
    return "Other/Unknown"


def group_education_goal(value: str) -> str:
    if value in TRANSFER_GOALS:
        return "Transfer-Oriented"
    if value in DEGREE_GOALS:
        return "Associate Degree"
    if value in CAREER_ED_GOALS:
        return "Certificate/Vocational"
    return "Other"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an interpretive cohort dataset.")
    parser.add_argument("--input", required=True, help="Path to primary analysis cohort CSV.")
    parser.add_argument("--output", required=True, help="Path to grouped output CSV.")
    parser.add_argument("--summary", required=True, help="Path to markdown summary output.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    df["residency_grouped"] = df["residency"].map(group_residency)
    df["ethnicity_grouped"] = df["ipeds_ethnicity"].map(group_ethnicity)
    df["gender_grouped"] = df["gender"].map(group_gender)
    df["education_goal_grouped"] = df["education_goal"].map(group_education_goal)

    summary_lines = [
        "# Interpretive Dataset Summary",
        "",
        f"- Rows: `{len(df):,}`",
        "",
        "## Grouped Variables",
        "",
        "### residency_grouped",
    ]
    for value, count in df["residency_grouped"].value_counts().items():
        summary_lines.append(f"- `{value}`: `{count}`")

    summary_lines.extend(["", "### ethnicity_grouped"])
    for value, count in df["ethnicity_grouped"].value_counts().items():
        summary_lines.append(f"- `{value}`: `{count}`")

    summary_lines.extend(["", "### gender_grouped"])
    for value, count in df["gender_grouped"].value_counts().items():
        summary_lines.append(f"- `{value}`: `{count}`")

    summary_lines.extend(["", "### education_goal_grouped"])
    for value, count in df["education_goal_grouped"].value_counts().items():
        summary_lines.append(f"- `{value}`: `{count}`")

    output_path = Path(args.output)
    summary_path = Path(args.summary)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"Wrote interpretive dataset to {output_path}")
    print(f"Wrote summary to {summary_path}")


if __name__ == "__main__":
    main()
