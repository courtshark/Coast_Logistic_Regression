# Current Methods Summary

## Study Objective

Estimate which student characteristics are associated with completing a degree within 3 academic years for the Fall 2021 entry cohort.

## Outcome

- `degree_obtained`
- Binary coding: `1 = completed degree within the Fall 2021 to Spring 2024 window`, `0 = did not complete within that window`

## Current Study Population

The primary analysis cohort includes students who meet both conditions:

1. `attendance_status` is `FT` or `PT`
2. `education_goal` is degree, certificate, or transfer-oriented

Excluded from the primary cohort:

- `WD` students because `WD` represents non-credit students
- students whose education goal is outside the degree/certificate/transfer pathway

## Current Cohort Size

- Raw cohort rows: `3,613`
- Primary analysis cohort rows: `3,140`

## Outcome Window

- Entry cohort: `Fall 2021`
- Completion deadline: `end of Spring 2024`
- Outcome framing: `completed within 3 academic years`

## Current Interpretable Model

Model type:

- logistic regression via `statsmodels` GLM with binomial family

Predictors currently included:

- `age`
- `attendance_status`
- `gender_grouped`
- `ethnicity_grouped`
- `residency_grouped`
- `athlete`
- `disability`
- `international_student`
- `district_status`
- `high_school_feeder`
- `bog_eligible`
- `education_goal_grouped`

## Grouping Decisions

- `gender_grouped`: `F`, `M`, `Other/Unknown`
- `ethnicity_grouped`: `Hispanic`, `Asian`, `White`, `Black`, `Other/Multiple/Unknown`
- `residency_grouped`: `California Resident`, `Nonresident/Foreign`, `AB540/Exempt/Other`
- `education_goal_grouped`: `Transfer-Oriented`, `Associate Degree`, `Certificate/Vocational`

## Variables Excluded From the Current Interpretable Model

- `student_id`
- `degree`
- `term_code`
- `term_semester`
- `student_type`
- `program_code`
- `program_description`
- `zipcode`
- `ethnicity_detail`
- `age_category`
- `foster_youth`
- `veteran`

## Current Model Performance

- Accuracy on full cohort: `0.689`
- ROC AUC on full cohort: `0.719`
- McFadden pseudo R-squared: `0.107`

## Current High-Level Interpretation

In the current model, stronger positive associations with 3-year completion include:

- full-time enrollment relative to part-time
- Asian ethnicity relative to Hispanic ethnicity
- BOG eligibility relative to non-eligibility
- feeder high school status relative to non-feeder high school status

Negative associations in the current model include:

- male students relative to female students
- associate-degree-only goal relative to transfer-oriented goal

These are model-based associations and should not be interpreted as causal effects.
