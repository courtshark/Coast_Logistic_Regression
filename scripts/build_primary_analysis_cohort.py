#!/usr/bin/env python3
"""Build the primary analysis cohort for the degree attainment study."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


INCLUDED_GOALS = {
    "AA Degree w/Transfer Bach.",
    "AA Degree w/out Transfer",
    "Bachelor's Degree or higher",
    "Certificate Only",
    "Two Yr. Vocational Degree",
    "4 yr college student meet 4 yr",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the primary analysis cohort.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV data.")
    parser.add_argument("--output", required=True, help="Path to filtered CSV data.")
    parser.add_argument(
        "--summary",
        required=True,
        help="Path to a markdown summary of the filtering decisions.",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    starting_rows = len(df)

    filtered = df[df["attendance_status"].isin(["FT", "PT"])].copy()
    after_credit_filter = len(filtered)

    filtered = filtered[filtered["education_goal"].isin(INCLUDED_GOALS)].copy()
    final_rows = len(filtered)

    summary_lines = [
        "# Primary Analysis Cohort",
        "",
        "- Outcome: `degree_obtained`",
        "- Included attendance statuses: `FT`, `PT`",
        "- Excluded attendance status: `WD` (non-credit students)",
        "- Included education goals:",
    ]
    for goal in sorted(INCLUDED_GOALS):
        summary_lines.append(f"  - `{goal}`")
    summary_lines.extend(
        [
            "",
            f"- Starting rows: `{starting_rows:,}`",
            f"- Rows after credit-student filter: `{after_credit_filter:,}`",
            f"- Final rows after education-goal filter: `{final_rows:,}`",
            f"- Final degree attainment rate: `{filtered['degree_obtained'].mean():.3f}`",
        ]
    )

    output_path = Path(args.output)
    summary_path = Path(args.summary)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    filtered.to_csv(output_path, index=False)
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"Wrote filtered cohort to {output_path}")
    print(f"Wrote summary to {summary_path}")
    print(f"Rows: {final_rows:,}")


if __name__ == "__main__":
    main()
