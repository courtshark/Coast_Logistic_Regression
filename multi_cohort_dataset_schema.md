# Multi-Cohort Dataset Schema

## Purpose

This schema is for a combined student-level dataset that stacks multiple fall-entry cohorts into one file for 3-academic-year completion analysis.

Recommended use:

- build each fall cohort separately first
- confirm the 3-year outcome window for that cohort
- standardize the columns
- append all cohorts into one master dataset

## Unit of Analysis

- one row per student
- one cohort assignment per student

## Core Cohort Logic

Each student should belong to one fall-entry cohort only.

Examples:

- `Fall 2019` cohort tracked through `Spring 2022`
- `Fall 2020` cohort tracked through `Spring 2023`
- `Fall 2021` cohort tracked through `Spring 2024`
- `Fall 2022` cohort tracked through `Spring 2025`

## Required Columns

| Column | Type | Description |
| --- | --- | --- |
| `student_id` | string | De-identified student key |
| `entry_term_code` | string | Original entry term code |
| `entry_term_label` | string | Human-readable cohort label such as `Fall 2021` |
| `entry_year` | integer | Entry year such as `2021` |
| `term_semester` | string | Semester label, typically `Fall` |
| `completed_within_3_years` | integer | `1=yes`, `0=no` |
| `completion_window_end` | string | Final term used to define completion, such as `Spring 2024` |

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

## Required Outcome Definition

The combined dataset should use one consistent outcome rule:

- `completed_within_3_years = 1` if the student completed by the end of the cohort-specific 3-academic-year window
- `completed_within_3_years = 0` otherwise

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

## Build Order

1. Extract one cohort at a time.
2. Apply that cohort's 3-year completion rule.
3. Rename columns into the shared schema.
4. Check missingness and coding consistency.
5. Append cohorts into one master dataset.

## Recommended Final File Name

- `multi_cohort_completion_dataset.csv`

## Example Rows

| student_id | entry_term_label | entry_year | completed_within_3_years | completion_window_end | attendance_status | education_goal |
| --- | --- | --- | --- | --- | --- | --- |
| `10001` | `Fall 2019` | `2019` | `1` | `Spring 2022` | `FT` | `AA Degree w/Transfer Bach.` |
| `10002` | `Fall 2020` | `2020` | `0` | `Spring 2023` | `PT` | `Certificate Only` |
| `10003` | `Fall 2021` | `2021` | `1` | `Spring 2024` | `FT` | `Bachelor's Degree or higher` |

## Notes

- Keep the raw cohort extracts separate for auditing.
- Use the combined dataset for pooled modeling only after cohort-specific checks are complete.
- If COVID-era patterns appear materially different, compare cohorts separately before pooling.
