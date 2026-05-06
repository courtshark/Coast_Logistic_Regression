# Logistic Model Report

- Outcome: `degree_obtained`
- Rows used: `3,140`
- Train rows: `2,512`
- Test rows: `628`
- Positive rate: `0.340`
- Accuracy: `0.696`
- ROC AUC: `0.705`

## Dropped Columns

- `age_category`
- `degree`
- `ethnicity_detail`
- `foster_youth`
- `program_code`
- `program_description`
- `student_id`
- `student_type`
- `term_code`
- `term_semester`
- `veteran`
- `zipcode`

## Top Positive Coefficients

- `categorical__ipeds_ethnicity_Asian`: `0.6195`
- `categorical__residency_Military Dependent NR Exempt`: `0.5287`
- `categorical__attendance_status_FT`: `0.4851`
- `categorical__residency_VACA Non-Resident Fee Exemptn`: `0.4798`
- `numeric__international_student`: `0.3941`
- `categorical__ipeds_ethnicity_Unknown`: `0.3404`
- `categorical__ipeds_ethnicity_White`: `0.3403`
- `categorical__high_school_feeder_Feeder HS`: `0.3116`
- `categorical__education_goal_4 yr college student meet 4 yr`: `0.2936`
- `categorical__education_goal_AA Degree w/Transfer Bach.`: `0.2089`

## Top Negative Coefficients

- `categorical__residency_Foreign`: `-0.9006`
- `categorical__ipeds_ethnicity_Pacific Islander`: `-0.8504`
- `categorical__attendance_status_PT`: `-0.7582`
- `categorical__ipeds_ethnicity_Black`: `-0.7563`
- `categorical__education_goal_AA Degree w/out Transfer`: `-0.4958`
- `categorical__high_school_feeder_Unknown`: `-0.4704`
- `categorical__education_goal_Bachelor's Degree or higher`: `-0.3779`
- `categorical__bog_eligible_No`: `-0.3525`
- `categorical__residency_California Resident`: `-0.3205`
- `categorical__gender_M`: `-0.3082`
