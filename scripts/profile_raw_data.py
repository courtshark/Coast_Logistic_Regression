#!/usr/bin/env python3
"""Profile the raw cohort workbook and write a markdown summary."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def build_markdown(df: pd.DataFrame, source_name: str) -> str:
    lines: list[str] = []
    lines.append("# Raw Data Profile")
    lines.append("")
    lines.append(f"- Source file: `{source_name}`")
    lines.append(f"- Rows: `{len(df):,}`")
    lines.append(f"- Columns: `{len(df.columns)}`")
    lines.append("")
    lines.append("## Columns")
    lines.append("")
    for column in df.columns:
        missing = int(df[column].isna().sum())
        non_null = df[column].dropna()
        dtype = str(df[column].dtype)
        unique_count = int(non_null.nunique())
        sample_values = [str(v) for v in non_null.astype(str).unique()[:5]]
        lines.append(
            f"- `{column}`: dtype=`{dtype}`, missing=`{missing}`, "
            f"unique_non_null=`{unique_count}`, sample={sample_values}"
        )

    lines.append("")
    lines.append("## Key Distributions")
    lines.append("")

    for column in ["Term_Code", "Term_Semester", "StudentType", "FT_PT", "Degree_obtained"]:
        if column in df.columns:
            lines.append(f"### {column}")
            lines.append("")
            counts = df[column].value_counts(dropna=False).head(20)
            for value, count in counts.items():
                label = "NA" if pd.isna(value) else str(value)
                lines.append(f"- `{label}`: `{count}`")
            lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile the raw cohort workbook.")
    parser.add_argument("--input", required=True, help="Path to the raw Excel workbook.")
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the markdown report to create.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    df = pd.read_excel(input_path)
    report = build_markdown(df, input_path.name)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"Wrote profile to {output_path}")


if __name__ == "__main__":
    main()
