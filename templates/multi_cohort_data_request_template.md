# Multi-Cohort Data Request Template

## Request Goal

Provide data for fall-entry cohorts to support a 3-academic-year completion analysis.

## Requested Cohorts

Please provide one extract for each cohort below, or one combined file with a clear cohort column:

- Fall 2019 with completion measured through Spring 2022
- Fall 2020 with completion measured through Spring 2023
- Fall 2021 with completion measured through Spring 2024
- Fall 2022 with completion measured through Spring 2025

## Preferred Data Structure

Please provide either:

1. a raw award/history table plus entry-cohort student attributes, or
2. a student-level rolled-up cohort table

Preferred modeling structure:

- one row per student
- one row per student's initial fall-entry cohort only
- no duplicate student rows in the final modeling file

If students can earn multiple degrees or certificates, keep those raw award rows in the source delivery and let the modeling file summarize them to one row per student.

## Recommended Raw Award / History Fields

- de-identified `student_id`
- `grad_term_code`
- `grad_academic_year`
- `degree_type`
- `degree_desc`
- `degree_status`
- `program`
- `program_desc`
- `min_term_enrolled`
- `max_term_enrolled`
- `ENGL100plus_Min_Term_Success`
- `MATH100plus_Min_Term_Success`

## Required Student-Level Modeling Fields

- de-identified `student_id`
- `entry_term_code`
- `entry_term_label`
- `entry_year`
- `term_semester`
- `completed_within_3_years`
- `completed_degree_within_3_years`
- `completed_any_award_within_3_years`
- `completion_window_end`
- `first_grad_term_code`
- `first_grad_academic_year`
- `award_count_within_3_years`
- `highest_award_level_within_3_years`

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
- `engl100plus_first_success_term`
- `math100plus_first_success_term`
- `ever_succeeded_engl100plus`
- `ever_succeeded_math100plus`
- `engl100plus_succeeded_in_first_term`
- `math100plus_succeeded_in_first_term`
- `engl100plus_succeeded_within_first_year`
- `math100plus_succeeded_within_first_year`

## Outcome Definition

Use this binary definition consistently:

- `completed_within_3_years = 1` if the student completed by the end of the cohort's 3-academic-year window
- `completed_within_3_years = 0` otherwise

Recommended student-level rollups:

- `completed_degree_within_3_years = 1` if a degree was earned by the deadline
- `completed_any_award_within_3_years = 1` if any degree or certificate was earned by the deadline
- `award_count_within_3_years` = count of awards earned by the deadline

## Delivery Notes

- Please standardize codes where possible across cohorts.
- If a field changed meaning across years, document that separately.
- If there are known COVID-era disruptions or coding changes, include that note with the delivery.
- Please clarify whether English and math success fields contain a term code or a yes/no flag.
- If English and math success are stored as term codes, do not pre-convert them unless that rule is documented.

## Preferred Output

- one raw CSV per cohort, or
- one combined raw CSV with cohort-identifying fields, plus
- one student-level rolled-up CSV if already available

Suggested final combined file name:

- `multi_cohort_completion_dataset.csv`
