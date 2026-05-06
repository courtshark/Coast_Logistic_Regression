# Data Dictionary

## Current Study Definition

- Primary outcome: `degree_obtained`
- Outcome meaning: binary indicator for whether the student obtained a degree
- Current cohort file: `data/raw/cohort.xlsx`
- Current cohort coverage: one fall cohort only (`Term_Code = 202170`)
- Unit of analysis: one row per student
- Primary analysis population: credit students (`FT` or `PT`) whose education goal is degree, certificate, or transfer-oriented

## Primary Analysis Cohort Rule

Include students only if both conditions are true:

1. `attendance_status` is `FT` or `PT`
2. `education_goal` is one of:
- `AA Degree w/Transfer Bach.`
- `AA Degree w/out Transfer`
- `Bachelor's Degree or higher`
- `Certificate Only`
- `Two Yr. Vocational Degree`
- `4 yr college student meet 4 yr`

Exclude:

- `attendance_status = WD` because this represents non-credit students
- students with non-award goals such as basic skills, personal interest, GED credits, career exploration, or undecided goals

## Variable Roles

| Original Column | Clean Column | Role | Type | Notes |
| --- | --- | --- | --- | --- |
| `Term_Code` | `term_code` | cohort field | categorical | Constant in current file; useful once additional cohorts are added |
| `Term_Semester` | `term_semester` | cohort field | categorical | Constant in current file; all rows are fall |
| `Student ID` | `student_id` | identifier | string | Private identifier; exclude from modeling |
| `Degree` | `degree` | excluded | categorical | Likely leaks outcome or reflects post-entry achievement; should stay out of baseline model |
| `StudentType` | `student_type` | scope field | categorical | Constant in current file: first-time college student |
| `Gender` | `gender` | predictor | categorical | Values include `F`, `M`, `N`, `B` |
| `IPEDS_Ethn` | `ipeds_ethnicity` | predictor | categorical | Broad race/ethnicity grouping |
| `Ethn_Detail` | `ethnicity_detail` | predictor candidate | categorical | More granular ethnicity; consider whether detail level is too sparse |
| `age_cat` | `age_category` | predictor | categorical | Age bands |
| `Residency` | `residency` | predictor | categorical | Includes California resident, foreign, out-of-state, and waiver categories |
| `Athlete` | `athlete` | predictor | binary | Encoded as `0/1` |
| `Disability` | `disability` | predictor | binary | Converted from `Y/N` to `1/0` |
| `FosterYouth` | `foster_youth` | predictor candidate | binary | Very low-frequency variable; may need careful handling |
| `Intl_Stdnt` | `international_student` | predictor | binary | Converted from `Y/N` to `1/0` |
| `Veteran` | `veteran` | predictor candidate | binary | Very low-frequency variable; may need careful handling |
| `OCCProgram_Code` | `program_code` | predictor candidate | categorical | High-cardinality; likely keep either code or description, not both |
| `OCCProgram_Desc` | `program_description` | predictor candidate | categorical | High-cardinality duplicate of program coding concept |
| `distr` | `district_status` | predictor | categorical | In-district, out-of-district, unknown |
| `hs_feeder` | `high_school_feeder` | predictor | categorical | Feeder, non-feeder, unknown |
| `BOG_Elig` | `bog_eligible` | predictor | categorical | Current values are `Yes/No` |
| `ED_GOAL` | `education_goal` | predictor | categorical | Strongly relevant but may need grouped categories |
| `AGE` | `age` | predictor | numeric | Continuous age at entry |
| `FT_PT` | `attendance_status` | predictor | categorical | Includes `FT`, `PT`, and `WD`; `WD` represents non-credit students |
| `ZIPCODE` | `zipcode` | predictor candidate | categorical | High-cardinality; consider grouping, geography mapping, or exclusion |
| `Degree_obtained` | `degree_obtained` | outcome | binary | Primary study outcome |

## Current Coding Notes

- `degree_obtained`: `0 = no`, `1 = yes`
- `athlete`: `0 = no`, `1 = yes`
- `disability`: converted to `0/1`
- `foster_youth`: converted to `0/1`
- `international_student`: converted to `0/1`
- `veteran`: `0 = no`, `1 = yes`
- `bog_eligible`: currently stored as `Yes/No`
- `attendance_status`: `FT = full-time`, `PT = part-time`, `WD = non-credit students`

## Modeling Notes

- `degree` should remain excluded from the baseline model because it is too close to the outcome and may introduce leakage.
- `program_code` and `program_description` represent the same concept twice. We should eventually keep only one.
- `zipcode`, `program_code`, `program_description`, and `ethnicity_detail` may create sparse categories and unstable coefficients.
- `student_type`, `term_code`, and `term_semester` are constant in the current file, so they do not help in the current single-cohort model.
- `foster_youth` and `veteran` are low-frequency predictors and may need grouped handling or careful interpretation.
- Because `WD` represents non-credit students rather than a standard enrollment intensity, those rows are excluded from the primary degree attainment model.

## Recommended Baseline Feature Set

These are the variables I would keep in the first defensible model:

- `gender`
- `ipeds_ethnicity`
- `age`
- `age_category`
- `residency`
- `athlete`
- `disability`
- `international_student`
- `district_status`
- `high_school_feeder`
- `bog_eligible`
- `education_goal`
- `attendance_status`

## Variables To Revisit After Baseline

- `ethnicity_detail`
- `foster_youth`
- `veteran`
- `program_code`
- `program_description`
- `zipcode`

## Next Decisions

1. Decide whether to use `age` or `age_category` in the primary model, but not both unless we have a strong reason.
2. Decide whether non-credit (`WD`) students should be excluded from the primary degree attainment model.
3. Decide whether `program` should be included in the first formal model.
4. Decide whether to group `education_goal` into fewer categories.
