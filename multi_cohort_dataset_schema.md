# Multi-Cohort Dataset Schema

## Purpose

This schema is for a combined student-level dataset that stacks multiple fall-entry cohorts into one file for 3-academic-year completion analysis.

Recommended use:

- build each fall cohort separately first
- confirm the 3-year outcome window for that cohort
- standardize the columns
- append all cohorts into one master dataset

This design assumes two related data layers:

1. a raw award-level or student-history source table
2. a student-level rolled-up modeling table

The model-ready dataset should always be student-level, not one row per award.

## Unit of Analysis

- one row per student
- one cohort assignment per student

If a student earned multiple degrees or certificates, those awards should be acknowledged in derived summary fields rather than by repeating the student across multiple modeling rows.

## Core Cohort Logic

Each student should belong to one fall-entry cohort only.

Examples:

- `Fall 2019` cohort tracked through `Spring 2022`
- `Fall 2020` cohort tracked through `Spring 2023`
- `Fall 2021` cohort tracked through `Spring 2024`
- `Fall 2022` cohort tracked through `Spring 2025`

## Required Columns In The Student-Level Modeling Table

| Column | Type | Description |
| --- | --- | --- |
| `student_id` | string | De-identified student key |
| `entry_term_code` | string | Original entry term code |
| `entry_term_label` | string | Human-readable cohort label such as `Fall 2021` |
| `entry_year` | integer | Entry year such as `2021` |
| `term_semester` | string | Semester label, typically `Fall` |
| `completed_within_3_years` | integer | `1=yes`, `0=no`; any primary completion outcome used for the study |
| `completed_degree_within_3_years` | integer | `1=yes`, `0=no`; recommended primary outcome if the study focuses on degrees |
| `completed_any_award_within_3_years` | integer | `1=yes`, `0=no`; degree or certificate earned within the window |
| `completion_window_end` | string | Final term used to define completion, such as `Spring 2024` |
| `first_grad_term_code` | string | Earliest graduation term within the completion window, if any |
| `first_grad_academic_year` | string | Academic year of the earliest completion within the window, if any |
| `award_count_within_3_years` | integer | Number of awards earned within the 3-year window |
| `highest_award_level_within_3_years` | string | Highest award type earned within the window, if defined locally |

## Recommended Predictor Columns

These should reflect information known at entry, unless explicitly documented otherwise.

| Column | Type | Description |
| --- | --- | --- |
| `student_type` | string | First-time college, transfer, etc. |
| `gender` | string | Student gender category |
| `ipeds_ethnicity` | string | Broad ethnicity category |
| `ethnicity_detail` | string | Detailed ethnicity category if available |
| `age` | numeric | Age at entry |
| `age_category` | string | Age band at entry |
| `residency` | string | Residency category |
| `attendance_status` | string | `FT`, `PT`, or other local coding |
| `athlete` | integer | `1=yes`, `0=no` |
| `disability` | integer | `1=yes`, `0=no` |
| `foster_youth` | integer | `1=yes`, `0=no` |
| `international_student` | integer | `1=yes`, `0=no` |
| `veteran` | integer | `1=yes`, `0=no` |
| `district_status` | string | In-district, out-of-district, etc. |
| `high_school_feeder` | string | Feeder high school indicator |
| `bog_eligible` | string | Financial aid eligibility indicator |
| `education_goal` | string | Declared education goal |
| `program_code` | string | Program code at entry |
| `program_description` | string | Program description at entry |
| `zipcode` | string | ZIP code if approved for use |

## Recommended Early Academic Derived Predictors

These are especially useful if you want an early-alert or post-first-term support model.

| Column | Type | Description |
| --- | --- | --- |
| `engl100plus_first_success_term` | string | Raw term code of first English success, kept for auditing |
| `math100plus_first_success_term` | string | Raw term code of first math success, kept for auditing |
| `ever_succeeded_engl100plus` | integer | `1=yes`, `0=no` |
| `ever_succeeded_math100plus` | integer | `1=yes`, `0=no` |
| `engl100plus_succeeded_in_first_term` | integer | `1=yes`, `0=no` |
| `math100plus_succeeded_in_first_term` | integer | `1=yes`, `0=no` |
| `engl100plus_succeeded_within_first_year` | integer | `1=yes`, `0=no` |
| `math100plus_succeeded_within_first_year` | integer | `1=yes`, `0=no` |

Do not use the raw success term code itself as a direct numeric predictor. Use derived flags instead.

## Required Outcome Definition

The combined dataset should use one consistent outcome rule:

- `completed_within_3_years = 1` if the student completed by the end of the cohort-specific 3-academic-year window
- `completed_within_3_years = 0` otherwise

Recommended refinement:

- `completed_degree_within_3_years = 1` if a degree was earned by the deadline
- `completed_any_award_within_3_years = 1` if any degree or certificate was earned by the deadline

Example:

- `Fall 2021` entrant
- completion deadline: `end of Spring 2024`
- if degree earned by that deadline: `1`

## Cohort-Specific Outcome Windows

Document the exact deadline used for each cohort.

Suggested columns:

- `entry_term_label`
- `completion_window_end`

This avoids confusion when combining cohorts across COVID and post-COVID periods.

## Raw Award Table Guidance

If the source system contains multiple rows per student because students can earn multiple awards, keep that raw table separate.

Recommended raw award fields:

- `student_id`
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

Use the raw table to derive student-level rollups.

## Student-Level Rollup Guidance

From the raw award table, derive one row per student with fields such as:

- `completed_degree_within_3_years`
- `completed_any_award_within_3_years`
- `first_grad_term_code`
- `first_grad_academic_year`
- `award_count_within_3_years`
- `engl100plus_first_success_term`
- `math100plus_first_success_term`
- first-term/first-year English and math success flags

## Build Order

1. Extract one cohort at a time.
2. Keep the raw award/history table for auditing.
3. Roll up the raw table to one student row per cohort.
4. Apply that cohort's 3-year completion rule.
5. Rename columns into the shared schema.
6. Check missingness and coding consistency.
7. Append cohorts into one master dataset.

## Recommended Final File Name

- `multi_cohort_completion_dataset.csv`

## Example Rows

| student_id | entry_term_label | entry_year | completed_degree_within_3_years | completed_any_award_within_3_years | award_count_within_3_years | completion_window_end | attendance_status | education_goal |
| --- | --- | --- | --- | --- | --- | --- |
| `10001` | `Fall 2019` | `2019` | `1` | `1` | `2` | `Spring 2022` | `FT` | `AA Degree w/Transfer Bach.` |
| `10002` | `Fall 2020` | `2020` | `0` | `1` | `1` | `Spring 2023` | `PT` | `Certificate Only` |
| `10003` | `Fall 2021` | `2021` | `1` | `1` | `4` | `Spring 2024` | `FT` | `Bachelor's Degree or higher` |

## Notes

- Keep the raw cohort extracts separate for auditing.
- Keep the raw award/history table separate from the final student-level modeling table.
- Use the combined dataset for pooled modeling only after cohort-specific checks are complete.
- If COVID-era patterns appear materially different, compare cohorts separately before pooling.
