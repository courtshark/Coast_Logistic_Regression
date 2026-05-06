#!/usr/bin/env python3
"""Score students for degree-attainment risk using the current statsmodels model."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


FORMULA = """
degree_obtained ~ age
    + C(attendance_status, Treatment(reference='PT'))
    + C(gender_grouped, Treatment(reference='F'))
    + C(ethnicity_grouped, Treatment(reference='Hispanic'))
    + C(residency_grouped, Treatment(reference='California Resident'))
    + athlete
    + disability
    + international_student
    + C(district_status, Treatment(reference='In-District'))
    + C(high_school_feeder, Treatment(reference='Not a Feeder HS'))
    + C(bog_eligible, Treatment(reference='No'))
    + C(education_goal_grouped, Treatment(reference='Transfer-Oriented'))
"""


def assign_risk_tier(risk_probability: float) -> str:
    if risk_probability >= 0.70:
        return "High"
    if risk_probability >= 0.40:
        return "Medium"
    return "Low"


def main() -> None:
    parser = argparse.ArgumentParser(description="Score at-risk students.")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the grouped interpretive cohort CSV.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the scored CSV file to create.",
    )
    parser.add_argument(
        "--summary",
        required=True,
        help="Path to the markdown scoring summary to create.",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    model = smf.glm(formula=FORMULA, data=df, family=sm.families.Binomial())
    result = model.fit()

    scored = df.copy()
    scored["predicted_degree_probability"] = result.predict(df)
    scored["risk_of_non_completion"] = 1 - scored["predicted_degree_probability"]
    scored["risk_tier"] = scored["risk_of_non_completion"].map(assign_risk_tier)
    scored["risk_percentile"] = scored["risk_of_non_completion"].rank(pct=True)

    output_columns = [
        "student_id",
        "term_code",
        "degree_obtained",
        "attendance_status",
        "education_goal",
        "predicted_degree_probability",
        "risk_of_non_completion",
        "risk_percentile",
        "risk_tier",
    ]
    available_columns = [column for column in output_columns if column in scored.columns]
    scored_for_export = scored[available_columns + [c for c in scored.columns if c not in available_columns]]

    summary_lines = [
        "# At-Risk Scoring Summary",
        "",
        "- Purpose: identify students for extra outreach and support",
        "- Use guidance: support planning only, not punitive or exclusionary decisions",
        "",
        "## Risk Tier Rule",
        "",
        "- `High`: risk of non-completion >= 0.70",
        "- `Medium`: risk of non-completion >= 0.40 and < 0.70",
        "- `Low`: risk of non-completion < 0.40",
        "",
        "## Tier Counts",
        "",
    ]

    tier_counts = scored["risk_tier"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0)
    for tier, count in tier_counts.items():
        summary_lines.append(f"- `{tier}`: `{count}`")

    summary_lines.extend(
        [
            "",
            "## Highest-Risk Students",
            "",
        ]
    )

    top_risk = scored.sort_values("risk_of_non_completion", ascending=False).head(10)
    for row in top_risk.itertuples(index=False):
        summary_lines.append(
            f"- `student_id={row.student_id}`: "
            f"risk_of_non_completion=`{row.risk_of_non_completion:.3f}`, "
            f"education_goal=`{row.education_goal}`, attendance_status=`{row.attendance_status}`"
        )

    output_path = Path(args.output)
    summary_path = Path(args.summary)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    scored_for_export.to_csv(output_path, index=False)
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"Wrote scored cohort to {output_path}")
    print(f"Wrote summary to {summary_path}")
    print("Tier counts:")
    print(tier_counts.to_string())


if __name__ == "__main__":
    main()
