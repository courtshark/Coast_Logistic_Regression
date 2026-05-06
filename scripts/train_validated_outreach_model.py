#!/usr/bin/env python3
"""Train and validate an outreach-focused risk model with a train/test split."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DEFAULT_FEATURES = [
    "age",
    "attendance_status",
    "athlete",
    "district_status",
    "high_school_feeder",
    "bog_eligible",
    "education_goal_grouped",
]

SENSITIVE_FEATURES = [
    "gender_grouped",
    "ethnicity_grouped",
    "residency_grouped",
    "disability",
    "international_student",
]


def assign_percentile_tier(risk_rank_percentile: float) -> str:
    if risk_rank_percentile <= 0.10:
        return "High"
    if risk_rank_percentile <= 0.30:
        return "Medium"
    return "Low"


def build_pipeline(feature_df: pd.DataFrame) -> Pipeline:
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a validated outreach risk model.")
    parser.add_argument("--input", required=True, help="Path to grouped cohort CSV.")
    parser.add_argument("--output", required=True, help="Path to scored cohort CSV.")
    parser.add_argument("--report", required=True, help="Path to markdown report.")
    parser.add_argument(
        "--include-sensitive",
        action="store_true",
        help="Include grouped demographic and other sensitive features in the outreach model.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of rows to reserve for testing. Default: 0.2",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for train/test split. Default: 42",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input).copy()
    features = DEFAULT_FEATURES.copy()
    if args.include_sensitive:
        features.extend(SENSITIVE_FEATURES)
    features = [feature for feature in features if feature in df.columns]

    X = df[features].copy()
    y = df["degree_obtained"].astype(int)

    X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(
        X,
        y,
        df.index,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y,
    )

    model = build_pipeline(X)
    model.fit(X_train, y_train)

    test_prob = model.predict_proba(X_test)[:, 1]
    test_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, test_pred)
    roc_auc = roc_auc_score(y_test, test_prob)
    precision = precision_score(y_test, test_pred, zero_division=0)
    recall = recall_score(y_test, test_pred, zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y_test, test_pred).ravel()

    all_prob = model.predict_proba(X)[:, 1]
    scored = df.copy()
    scored["predicted_degree_probability_validated"] = all_prob
    scored["risk_of_non_completion_validated"] = 1 - scored["predicted_degree_probability_validated"]
    scored["risk_rank_percentile"] = scored["risk_of_non_completion_validated"].rank(
        method="average", ascending=False, pct=True
    )
    scored["risk_tier_validated"] = scored["risk_rank_percentile"].map(assign_percentile_tier)
    scored["was_in_test_set"] = False
    scored.loc[test_idx, "was_in_test_set"] = True

    output_columns = [
        "student_id",
        "term_code",
        "degree_obtained",
        "attendance_status",
        "education_goal",
        "predicted_degree_probability_validated",
        "risk_of_non_completion_validated",
        "risk_rank_percentile",
        "risk_tier_validated",
        "was_in_test_set",
    ]
    available_columns = [column for column in output_columns if column in scored.columns]
    scored = scored[available_columns + [c for c in scored.columns if c not in available_columns]]

    tier_counts = scored["risk_tier_validated"].value_counts().reindex(
        ["High", "Medium", "Low"], fill_value=0
    )
    top_risk = scored.sort_values("risk_of_non_completion_validated", ascending=False).head(10)

    summary_lines = [
        "# Validated Outreach Risk Model",
        "",
        "- Purpose: identify students for extra outreach and support using a validated model",
        "- Modeling approach: train/test split with stratification on `degree_obtained`",
        "- Use guidance: support planning only, not punitive or exclusionary decisions",
        "",
        "## Feature Set",
        "",
        f"- Included features: `{', '.join(features)}`",
        f"- Sensitive features included: `{args.include_sensitive}`",
        "",
        "## Test-Set Metrics",
        "",
        f"- Test rows: `{len(X_test):,}`",
        f"- Accuracy: `{accuracy:.3f}`",
        f"- ROC AUC: `{roc_auc:.3f}`",
        f"- Precision: `{precision:.3f}`",
        f"- Recall: `{recall:.3f}`",
        "",
        "## Test-Set Confusion Matrix",
        "",
        f"- True negatives: `{tn}`",
        f"- False positives: `{fp}`",
        f"- False negatives: `{fn}`",
        f"- True positives: `{tp}`",
        "",
        "## Risk Tier Rule",
        "",
        "- `High`: top 10% highest risk of non-completion",
        "- `Medium`: next 20% highest risk of non-completion",
        "- `Low`: remaining 70%",
        "",
        "## Tier Counts",
        "",
    ]

    for tier, count in tier_counts.items():
        summary_lines.append(f"- `{tier}`: `{count}`")

    summary_lines.extend(["", "## Highest-Risk Students", ""])
    for row in top_risk.itertuples(index=False):
        summary_lines.append(
            f"- `student_id={row.student_id}`: "
            f"risk_of_non_completion=`{row.risk_of_non_completion_validated:.3f}`, "
            f"education_goal=`{row.education_goal}`, attendance_status=`{row.attendance_status}`"
        )

    output_path = Path(args.output)
    report_path = Path(args.report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    scored.to_csv(output_path, index=False)
    write_text(report_path, "\n".join(summary_lines) + "\n")

    print(f"Wrote scored cohort to {output_path}")
    print(f"Wrote report to {report_path}")
    print(f"ROC AUC: {roc_auc:.3f}")
    print("Tier counts:")
    print(tier_counts.to_string())


if __name__ == "__main__":
    main()
