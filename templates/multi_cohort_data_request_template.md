# Multi-Cohort Data Request Template

## Request Goal

Provide a student-level file for fall-entry cohorts to support a 3-academic-year completion analysis.

## Requested Cohorts

Please provide one extract for each cohort below, or one combined file with a clear cohort column:

- Fall 2019 with completion measured through Spring 2022
- Fall 2020 with completion measured through Spring 2023
- Fall 2021 with completion measured through Spring 2024
- Fall 2022 with completion measured through Spring 2025

## Unit of Analysis

- one row per student
- one row per student's initial fall-entry cohort only

## Required Fields

- de-identified `student_id`
- `entry_term_code`
- `entry_term_label`
- `entry_year`
- `term_semester`
- `completed_within_3_years`
- `completion_window_end`

## Recommended Predictor Fields

- `student_type`
- `gender`
- `ipeds_ethnicity`
- `ethnicity_detail`
- `age`
- `age_category`
- `residency`
- `attendance_status`
- `athlete`
- `disability`
- `foster_youth`
- `international_student`
- `veteran`
- `district_status`
- `high_school_feeder`
- `bog_eligible`
- `education_goal`
- `program_code`
- `program_description`
- `zipcode` if approved for analysis

## Outcome Definition

Use this binary definition consistently:

- `completed_within_3_years = 1` if the student completed by the end of the cohort's 3-academic-year window
- `completed_within_3_years = 0` otherwise

## Delivery Notes

- Please standardize codes where possible across cohorts.
- If a field changed meaning across years, document that separately.
- If there are known COVID-era disruptions or coding changes, include that note with the delivery.

## Preferred Output

- one CSV per cohort, or
- one combined CSV with a cohort field

Suggested final combined file name:

- `multi_cohort_completion_dataset.csv`
