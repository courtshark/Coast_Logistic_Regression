#!/usr/bin/env python3
"""Fit an interpretable logistic regression model with statsmodels."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import accuracy_score, roc_auc_score


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Fit an interpretable logistic regression model.")
    parser.add_argument("--input", required=True, help="Path to grouped cohort CSV.")
    parser.add_argument("--report", required=True, help="Path to markdown report.")
    parser.add_argument("--coefficients", required=True, help="Path to coefficient CSV.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    model = smf.glm(formula=FORMULA, data=df, family=sm.families.Binomial())
    result = model.fit()

    predicted_prob = result.predict(df)
    predicted_class = (predicted_prob >= 0.5).astype(int)
    accuracy = accuracy_score(df["degree_obtained"], predicted_class)
    roc_auc = roc_auc_score(df["degree_obtained"], predicted_prob)

    null_model = smf.glm("degree_obtained ~ 1", data=df, family=sm.families.Binomial()).fit()
    mcfadden_r2 = 1 - (result.llf / null_model.llf)

    conf = result.conf_int()
    coef_df = pd.DataFrame(
        {
            "term": result.params.index,
            "coefficient": result.params.values,
            "odds_ratio": np.exp(result.params.values),
            "ci_lower_odds_ratio": np.exp(conf[0].values),
            "ci_upper_odds_ratio": np.exp(conf[1].values),
            "p_value": result.pvalues.values,
        }
    ).sort_values("p_value")

    top_terms = coef_df[coef_df["term"] != "Intercept"].head(15)

    lines = [
        "# Statsmodels Logistic Regression Report",
        "",
        "- Outcome: `degree_obtained`",
        "- Dataset: grouped primary analysis cohort",
        f"- Rows used: `{len(df):,}`",
        f"- Accuracy on full cohort: `{accuracy:.3f}`",
        f"- ROC AUC on full cohort: `{roc_auc:.3f}`",
        f"- McFadden pseudo R-squared: `{mcfadden_r2:.3f}`",
        "",
        "## Model Formula",
        "",
        "```",
        "degree_obtained ~ age + attendance_status + gender_grouped + ethnicity_grouped +",
        "residency_grouped + athlete + disability + international_student +",
        "district_status + high_school_feeder + bog_eligible + education_goal_grouped",
        "```",
        "",
        "## Most Statistically Informative Terms",
        "",
    ]

    for row in top_terms.itertuples(index=False):
        lines.append(
            f"- `{row.term}`: OR=`{row.odds_ratio:.3f}`, "
            f"95% CI=`({row.ci_lower_odds_ratio:.3f}, {row.ci_upper_odds_ratio:.3f})`, "
            f"p=`{row.p_value:.4f}`"
        )

    report_path = Path(args.report)
    coef_path = Path(args.coefficients)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    coef_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    coef_df.to_csv(coef_path, index=False)

    print(f"Wrote report to {report_path}")
    print(f"Wrote coefficients to {coef_path}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"ROC AUC: {roc_auc:.3f}")
    print(f"McFadden R2: {mcfadden_r2:.3f}")


if __name__ == "__main__":
    main()
