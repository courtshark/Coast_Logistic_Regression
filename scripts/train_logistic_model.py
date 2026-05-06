#!/usr/bin/env python3
"""Train a baseline logistic regression model on the cleaned cohort dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DEFAULT_EXCLUDE = {"student_id", "degree"}


def build_report(
    outcome: str,
    n_rows: int,
    train_rows: int,
    test_rows: int,
    accuracy: float,
    roc_auc: float,
    positive_rate: float,
    dropped_columns: list[str],
    top_positive: list[tuple[str, float]],
    top_negative: list[tuple[str, float]],
) -> str:
    lines: list[str] = []
    lines.append("# Logistic Model Report")
    lines.append("")
    lines.append(f"- Outcome: `{outcome}`")
    lines.append(f"- Rows used: `{n_rows:,}`")
    lines.append(f"- Train rows: `{train_rows:,}`")
    lines.append(f"- Test rows: `{test_rows:,}`")
    lines.append(f"- Positive rate: `{positive_rate:.3f}`")
    lines.append(f"- Accuracy: `{accuracy:.3f}`")
    lines.append(f"- ROC AUC: `{roc_auc:.3f}`")
    lines.append("")
    lines.append("## Dropped Columns")
    lines.append("")
    for column in dropped_columns:
        lines.append(f"- `{column}`")
    lines.append("")
    lines.append("## Top Positive Coefficients")
    lines.append("")
    for feature, coef in top_positive:
        lines.append(f"- `{feature}`: `{coef:.4f}`")
    lines.append("")
    lines.append("## Top Negative Coefficients")
    lines.append("")
    for feature, coef in top_negative:
        lines.append(f"- `{feature}`: `{coef:.4f}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a baseline logistic regression model.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV data.")
    parser.add_argument(
        "--outcome",
        default="degree_obtained",
        help="Binary outcome column to model.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Path to the markdown model report to write.",
    )
    parser.add_argument(
        "--coefficients",
        required=True,
        help="Path to the coefficient CSV to write.",
    )
    parser.add_argument(
        "--exclude-columns",
        default="",
        help="Comma-separated list of additional columns to exclude from modeling.",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    outcome = args.outcome

    if outcome not in df.columns:
        raise ValueError(f"Outcome column '{outcome}' not found.")

    df = df.dropna(subset=[outcome]).copy()
    df[outcome] = pd.to_numeric(df[outcome], errors="coerce")
    df = df.dropna(subset=[outcome]).copy()
    df[outcome] = df[outcome].astype(int)

    feature_df = df.drop(columns=[outcome])
    extra_excludes = {
        column.strip() for column in args.exclude_columns.split(",") if column.strip()
    }
    exclude_columns = DEFAULT_EXCLUDE | extra_excludes

    dropped_columns = sorted(
        [column for column in feature_df.columns if column in exclude_columns]
    )
    feature_df = feature_df.drop(columns=dropped_columns, errors="ignore")

    single_value_columns = [
        column for column in feature_df.columns if feature_df[column].nunique(dropna=False) <= 1
    ]
    dropped_columns.extend(single_value_columns)
    feature_df = feature_df.drop(columns=single_value_columns)

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

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=2000)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        feature_df,
        df[outcome],
        test_size=0.2,
        random_state=42,
        stratify=df[outcome],
    )

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    transformed_names = model.named_steps["preprocessor"].get_feature_names_out()
    coefficients = model.named_steps["classifier"].coef_[0]
    coef_df = pd.DataFrame(
        {
            "feature": transformed_names,
            "coefficient": coefficients,
            "odds_ratio": np.exp(coefficients),
        }
    ).sort_values("coefficient", ascending=False)

    top_positive = list(coef_df[["feature", "coefficient"]].head(10).itertuples(index=False, name=None))
    top_negative = list(
        coef_df[["feature", "coefficient"]]
        .sort_values("coefficient", ascending=True)
        .head(10)
        .itertuples(index=False, name=None)
    )

    report_text = build_report(
        outcome=outcome,
        n_rows=len(df),
        train_rows=len(X_train),
        test_rows=len(X_test),
        accuracy=accuracy,
        roc_auc=roc_auc,
        positive_rate=float(df[outcome].mean()),
        dropped_columns=sorted(set(dropped_columns)),
        top_positive=top_positive,
        top_negative=top_negative,
    )

    report_path = Path(args.report)
    coefficients_path = Path(args.coefficients)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    coefficients_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    coef_df.to_csv(coefficients_path, index=False)

    print(f"Wrote report to {report_path}")
    print(f"Wrote coefficients to {coefficients_path}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"ROC AUC: {roc_auc:.3f}")


if __name__ == "__main__":
    main()
