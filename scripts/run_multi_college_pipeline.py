#!/usr/bin/env python3
"""Run the reusable multi-college degree-attainment pipeline from config."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def standardize_strings(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        if pd.api.types.is_object_dtype(df[column]):
            df[column] = df[column].map(
                lambda value: value.strip() if isinstance(value, str) else value
            )
    return df


def normalize_binary_columns(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    for column in config.get("binary_columns_zero_one", []):
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    yn_map = {"Y": 1, "N": 0, "Yes": 1, "No": 0}
    for column in config.get("binary_columns_yes_no", []):
        if column in df.columns:
            df[column] = df[column].map(yn_map).astype("Int64")
    return df


def prepare_model_dataset(input_path: Path, mapping: dict, config: dict) -> pd.DataFrame:
    df = pd.read_excel(input_path)
    df = df.rename(columns=mapping)
    df = standardize_strings(df)
    df = normalize_binary_columns(df, config)

    for column in ["student_id", "term_code"]:
        if column in df.columns:
            df[column] = df[column].astype(str)
    return df


def build_primary_analysis_cohort(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    attendance_values = set(config["included_attendance_statuses"])
    education_goals = set(config["included_education_goals"])

    filtered = df[df["attendance_status"].isin(attendance_values)].copy()
    filtered = filtered[filtered["education_goal"].isin(education_goals)].copy()
    return filtered


def apply_grouping(series: pd.Series, group_map: dict) -> pd.Series:
    default_value = group_map.get("__default__", "Other")
    explicit_map = {k: v for k, v in group_map.items() if k != "__default__"}
    return series.map(lambda value: explicit_map.get(value, default_value))


def build_interpretive_dataset(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    grouped = df.copy()
    groupings = config["groupings"]
    grouped["residency_grouped"] = apply_grouping(grouped["residency"], groupings["residency"])
    grouped["ethnicity_grouped"] = apply_grouping(
        grouped["ipeds_ethnicity"], groupings["ipeds_ethnicity"]
    )
    grouped["gender_grouped"] = apply_grouping(grouped["gender"], groupings["gender"])
    grouped["education_goal_grouped"] = apply_grouping(
        grouped["education_goal"], groupings["education_goal"]
    )
    return grouped


def statsmodels_formula(outcome_column: str) -> str:
    return f"""
{outcome_column} ~ age
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


def fit_interpretive_model(df: pd.DataFrame, outcome_column: str) -> tuple[pd.DataFrame, dict]:
    formula = statsmodels_formula(outcome_column)
    model = smf.glm(formula=formula, data=df, family=sm.families.Binomial())
    result = model.fit()

    predicted_prob = result.predict(df)
    predicted_class = (predicted_prob >= 0.5).astype(int)
    accuracy = accuracy_score(df[outcome_column], predicted_class)
    roc_auc = roc_auc_score(df[outcome_column], predicted_prob)

    null_model = smf.glm(f"{outcome_column} ~ 1", data=df, family=sm.families.Binomial()).fit()
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
        "row_count": len(df),
        "accuracy": accuracy,
        "roc_auc": roc_auc,
        "mcfadden_r2": mcfadden_r2,
    }
    return coef_df, metrics


def build_outreach_pipeline(feature_df: pd.DataFrame) -> Pipeline:
    numeric_columns = feature_df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = [c for c in feature_df.columns if c not in numeric_columns]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_columns,
            ),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_columns,
            ),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=2000, solver="liblinear")),
        ]
    )


def assign_percentile_tier(risk_rank_percentile: float) -> str:
    if risk_rank_percentile <= 0.10:
        return "High"
    if risk_rank_percentile <= 0.30:
        return "Medium"
    return "Low"


def fit_validated_outreach_model(
    df: pd.DataFrame, outcome_column: str, config: dict, include_sensitive: bool
) -> tuple[pd.DataFrame, dict]:
    features = list(config["outreach_feature_columns"])
    if include_sensitive:
        features.extend(config.get("sensitive_outreach_feature_columns", []))
    features = [feature for feature in features if feature in df.columns]

    X = df[features].copy()
    y = df[outcome_column].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = build_outreach_pipeline(X)
    model.fit(X_train, y_train)

    test_prob = model.predict_proba(X_test)[:, 1]
    test_pred = model.predict(X_test)

    scored = df.copy()
    scored["predicted_degree_probability_validated"] = model.predict_proba(X)[:, 1]
    scored["risk_of_non_completion_validated"] = 1 - scored["predicted_degree_probability_validated"]
    scored["risk_rank_percentile"] = scored["risk_of_non_completion_validated"].rank(
        method="average", ascending=False, pct=True
    )
    scored["risk_tier_validated"] = scored["risk_rank_percentile"].map(assign_percentile_tier)

    metrics = {
        "features_used": features,
        "include_sensitive": include_sensitive,
        "test_rows": len(X_test),
        "accuracy": accuracy_score(y_test, test_pred),
        "roc_auc": roc_auc_score(y_test, test_prob),
        "precision": precision_score(y_test, test_pred, zero_division=0),
        "recall": recall_score(y_test, test_pred, zero_division=0),
    }
    return scored, metrics


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def methods_summary(metrics: dict, college_name: str) -> str:
    return "\n".join(
        [
            f"# {college_name} Methods Summary",
            "",
            "## Current Interpretable Model",
            "",
            "- logistic regression via `statsmodels` GLM with binomial family",
            "- grouped variables for residency, ethnicity, gender, and education goal",
            "",
            "## Performance",
            "",
            f"- Rows used: `{metrics['row_count']:,}`",
            f"- Accuracy on full cohort: `{metrics['accuracy']:.3f}`",
            f"- ROC AUC on full cohort: `{metrics['roc_auc']:.3f}`",
            f"- McFadden pseudo R-squared: `{metrics['mcfadden_r2']:.3f}`",
            "",
        ]
    ) + "\n"


def outreach_summary(metrics: dict, scored: pd.DataFrame, college_name: str) -> str:
    tier_counts = scored["risk_tier_validated"].value_counts().reindex(
        ["High", "Medium", "Low"], fill_value=0
    )
    lines = [
        f"# {college_name} Validated Outreach Risk Model",
        "",
        "- Purpose: identify students for extra outreach and support using a validated model",
        "- Modeling approach: train/test split with stratification on the chosen outcome",
        "",
        "## Test-Set Metrics",
        "",
        f"- Included features: `{', '.join(metrics['features_used'])}`",
        f"- Sensitive features included: `{metrics['include_sensitive']}`",
        f"- Test rows: `{metrics['test_rows']:,}`",
        f"- Accuracy: `{metrics['accuracy']:.3f}`",
        f"- ROC AUC: `{metrics['roc_auc']:.3f}`",
        f"- Precision: `{metrics['precision']:.3f}`",
        f"- Recall: `{metrics['recall']:.3f}`",
        "",
        "## Tier Counts",
        "",
    ]
    for tier, count in tier_counts.items():
        lines.append(f"- `{tier}`: `{count}`")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reusable multi-college pipeline.")
    parser.add_argument("--input", required=True, help="Path to raw Excel workbook.")
    parser.add_argument("--mapping-config", required=True, help="Path to column mapping JSON.")
    parser.add_argument("--college-config", required=True, help="Path to college config JSON.")
    parser.add_argument("--output-dir", required=True, help="Directory for outputs.")
    parser.add_argument(
        "--college-name",
        default="College",
        help="Display name for reports. Default: College",
    )
    parser.add_argument(
        "--include-sensitive-outreach-features",
        action="store_true",
        help="Include grouped demographic/sensitive features in the validated outreach model.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    mapping = load_json(Path(args.mapping_config))
    config = load_json(Path(args.college_config))
    output_dir = Path(args.output_dir)
    data_dir = output_dir / "data"
    reports_dir = output_dir / "reports"

    cleaned = prepare_model_dataset(input_path, mapping, config)
    primary = build_primary_analysis_cohort(cleaned, config)
    interpretive = build_interpretive_dataset(primary, config)
    coef_df, interpretive_metrics = fit_interpretive_model(interpretive, config["outcome_column"])
    validated_scored, outreach_metrics = fit_validated_outreach_model(
        interpretive,
        config["outcome_column"],
        config,
        args.include_sensitive_outreach_features,
    )

    data_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    cleaned.to_csv(data_dir / "cohort_model_dataset.csv", index=False)
    primary.to_csv(data_dir / "primary_analysis_cohort.csv", index=False)
    interpretive.to_csv(data_dir / "interpretive_primary_analysis_cohort.csv", index=False)
    validated_scored.to_csv(data_dir / "validated_scored_primary_analysis_cohort.csv", index=False)
    coef_df.to_csv(reports_dir / "statsmodels_degree_obtained_coefficients.csv", index=False)
    write_text(reports_dir / "methods_summary.md", methods_summary(interpretive_metrics, args.college_name))
    write_text(
        reports_dir / "validated_outreach_risk_model.md",
        outreach_summary(outreach_metrics, validated_scored, args.college_name),
    )

    print("Multi-college pipeline complete")
    print(f"College: {args.college_name}")
    print(f"Output directory: {output_dir}")
    print(f"Rows in primary cohort: {len(primary):,}")
    print(f"Interpretable model ROC AUC: {interpretive_metrics['roc_auc']:.3f}")
    print(f"Validated outreach ROC AUC: {outreach_metrics['roc_auc']:.3f}")


if __name__ == "__main__":
    main()
