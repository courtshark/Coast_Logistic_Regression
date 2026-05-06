#!/usr/bin/env python3
"""Create a cleaned modeling dataset from the raw cohort workbook."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a cleaned cohort dataset.")
    parser.add_argument("--input", required=True, help="Path to the raw Excel workbook.")
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the cleaned CSV file to create.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    df = pd.read_excel(input_path)
    df = df.rename(columns=RENAME_MAP)
    df = standardize_strings(df)
    df = normalize_binary_columns(df)

    if "student_id" in df.columns:
        df["student_id"] = df["student_id"].astype(str)

    if "term_code" in df.columns:
        df["term_code"] = df["term_code"].astype(str)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Wrote cleaned dataset to {output_path}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
