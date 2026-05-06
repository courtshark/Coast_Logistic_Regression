#!/usr/bin/env python3
"""Run the full degree attainment pipeline from a raw Excel file."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import accuracy_score, roc_auc_score


RENAME_MAP = {
    "Term_Code": "term_code",
    "Term_Semester": "term_semester",
    "Student ID": "student_id",
    "Degree": "degree",
    "StudentType": "student_type",
    "Gender": "gender",
    "IPEDS_Ethn": "ipeds_ethnicity",
    "Ethn_Detail": "ethnicity_detail",
    "age_cat": "age_category",
    "Residency": "residency",
    "Athlete": "athlete",
    "Disability": "disability",
    "FosterYouth": "foster_youth",
    "Intl_Stdnt": "international_student",
    "Veteran": "veteran",
    "OCCProgram_Code": "program_code",
    "OCCProgram_Desc": "program_description",
    "distr": "district_status",
    "hs_feeder": "high_school_feeder",
    "BOG_Elig": "bog_eligible",
    "ED_GOAL": "education_goal",
    "AGE": "age",
    "FT_PT": "attendance_status",
    "ZIPCODE": "zipcode",
    "Degree_obtained": "degree_obtained",
}

ZERO_ONE_COLUMNS = ["athlete", "veteran", "degree_obtained"]
YN_COLUMNS = ["disability", "foster_youth", "international_student"]

INCLUDED_GOALS = {
    "AA Degree w/Transfer Bach.",
    "AA Degree w/out Transfer",
    "Bachelor's Degree or higher",
    "Certificate Only",
    "Two Yr. Vocational Degree",
    "4 yr college student meet 4 yr",
}

TRANSFER_GOALS = {
    "AA Degree w/Transfer Bach.",
    "Bachelor's Degree or higher",
    "4 yr college student meet 4 yr",
}
DEGREE_GOALS = {"AA Degree w/out Transfer"}
CAREER_ED_GOALS = {"Certificate Only", "Two Yr. Vocational Degree"}

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


def standardize_strings(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if pd.api.types.is_object_dtype(df[column]):
            df[column] = df[column].map(
                lambda value: value.strip() if isinstance(value, str) else value
            )
    return df


def normalize_binary_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in ZERO_ONE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    yn_map = {"Y": 1, "N": 0, "Yes": 1, "No": 0}
    for column in YN_COLUMNS:
        if column in df.columns:
            df[column] = df[column].map(yn_map).astype("Int64")
    return df


def prepare_model_dataset(input_path: Path) -> pd.DataFrame:
    df = pd.read_excel(input_path)
    df = df.rename(columns=RENAME_MAP)
    df = standardize_strings(df)
    df = normalize_binary_columns(df)

    if "student_id" in df.columns:
        df["student_id"] = df["student_id"].astype(str)
    if "term_code" in df.columns:
        df["term_code"] = df["term_code"].astype(str)
    return df


def build_primary_analysis_cohort(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df[df["attendance_status"].isin(["FT", "PT"])].copy()
    filtered = filtered[filtered["education_goal"].isin(INCLUDED_GOALS)].copy()
    return filtered


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


def build_interpretive_dataset(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.copy()
    grouped["residency_grouped"] = grouped["residency"].map(group_residency)
    grouped["ethnicity_grouped"] = grouped["ipeds_ethnicity"].map(group_ethnicity)
    grouped["gender_grouped"] = grouped["gender"].map(group_gender)
    grouped["education_goal_grouped"] = grouped["education_goal"].map(group_education_goal)
    return grouped


def fit_statsmodels_model(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
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

    metrics = {
        "accuracy": accuracy,
        "roc_auc": roc_auc,
        "mcfadden_r2": mcfadden_r2,
        "row_count": len(df),
    }
    return coef_df, metrics


def assign_risk_tier(risk_probability: float) -> str:
    if risk_probability >= 0.70:
        return "High"
    if risk_probability >= 0.40:
        return "Medium"
    return "Low"


def score_students(df: pd.DataFrame) -> pd.DataFrame:
    model = smf.glm(formula=FORMULA, data=df, family=sm.families.Binomial())
    result = model.fit()

    scored = df.copy()
    scored["predicted_degree_probability"] = result.predict(df)
    scored["risk_of_non_completion"] = 1 - scored["predicted_degree_probability"]
    scored["risk_tier"] = scored["risk_of_non_completion"].map(assign_risk_tier)
    scored["risk_percentile"] = scored["risk_of_non_completion"].rank(pct=True)
    return scored


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_methods_summary(metrics: dict[str, float]) -> str:
    return "\n".join(
        [
            "# Current Methods Summary",
            "",
            "## Study Objective",
            "",
            "Estimate which student characteristics are associated with `degree_obtained`.",
            "",
            "## Current Study Population",
            "",
            "- credit students only (`FT` or `PT`)",
            "- degree-, certificate-, or transfer-oriented education goals only",
            "",
            "## Current Interpretable Model",
            "",
            "- logistic regression via `statsmodels` GLM with binomial family",
            "- grouped variables for residency, ethnicity, gender, and education goal",
            "",
            "## Current Model Performance",
            "",
            f"- Rows used: `{metrics['row_count']:,}`",
            f"- Accuracy on full cohort: `{metrics['accuracy']:.3f}`",
            f"- ROC AUC on full cohort: `{metrics['roc_auc']:.3f}`",
            f"- McFadden pseudo R-squared: `{metrics['mcfadden_r2']:.3f}`",
            "",
        ]
    ) + "\n"


def build_findings_summary(metrics: dict[str, float], coef_df: pd.DataFrame) -> str:
    top = coef_df[coef_df["term"] != "Intercept"].head(10)
    lines = [
        "# Stakeholder Findings Summary",
        "",
        "## Overview",
        "",
        "This summary highlights current findings from the degree attainment model.",
        "",
        f"- Students analyzed: `{metrics['row_count']:,}`",
        f"- Model ROC AUC: `{metrics['roc_auc']:.3f}`",
        f"- Model accuracy: `{metrics['accuracy']:.3f}`",
        "",
        "## Strongest Current Associations",
        "",
    ]
    for row in top.itertuples(index=False):
        lines.append(
            f"- `{row.term}`: OR=`{row.odds_ratio:.3f}`, "
            f"95% CI=`({row.ci_lower_odds_ratio:.3f}, {row.ci_upper_odds_ratio:.3f})`, "
            f"p=`{row.p_value:.4f}`"
        )
    lines.extend(
        [
            "",
            "## Interpretation Note",
            "",
            "These are associations from the current model and should not be interpreted as causal effects.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full degree attainment pipeline.")
    parser.add_argument("--input", required=True, help="Path to raw Excel workbook.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where processed data and reports should be written.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    data_dir = output_dir / "data"
    reports_dir = output_dir / "reports"

    cleaned = prepare_model_dataset(input_path)
    primary = build_primary_analysis_cohort(cleaned)
    interpretive = build_interpretive_dataset(primary)
    coef_df, metrics = fit_statsmodels_model(interpretive)
    scored = score_students(interpretive)

    data_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    cleaned.to_csv(data_dir / "cohort_model_dataset.csv", index=False)
    primary.to_csv(data_dir / "primary_analysis_cohort.csv", index=False)
    interpretive.to_csv(data_dir / "interpretive_primary_analysis_cohort.csv", index=False)
    scored.to_csv(data_dir / "scored_primary_analysis_cohort.csv", index=False)
    coef_df.to_csv(reports_dir / "statsmodels_degree_obtained_coefficients.csv", index=False)
    write_text(reports_dir / "methods_summary.md", build_methods_summary(metrics))
    write_text(reports_dir / "stakeholder_findings_summary.md", build_findings_summary(metrics, coef_df))

    print("Pipeline complete")
    print(f"Output directory: {output_dir}")
    print(f"Rows in primary cohort: {len(primary):,}")
    print(f"ROC AUC: {metrics['roc_auc']:.3f}")


if __name__ == "__main__":
    main()
