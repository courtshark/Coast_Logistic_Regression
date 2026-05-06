# Logistic Model Report

- Outcome: `degree_obtained`
- Rows used: `3,613`
- Train rows: `2,890`
- Test rows: `723`
- Positive rate: `0.318`
- Accuracy: `0.694`
- ROC AUC: `0.700`

## Dropped Columns

- `degree`
- `student_id`
- `student_type`
- `term_code`
- `term_semester`

## Top Positive Coefficients

- `categorical__ethnicity_detail_Asian - Japanese`: `0.9347`
- `categorical__program_code_1_CT_ATM`: `0.8065`
- `categorical__program_description_Airline Travel Management`: `0.8065`
- `categorical__program_description_Public Health-General Studies`: `0.7927`
- `categorical__program_code_1_AA_PUBG`: `0.7927`
- `categorical__education_goal_Prepare for a new career`: `0.7434`
- `categorical__program_code_1_CT_VRAR`: `0.7032`
- `categorical__program_description_Immersive Media (VR/AR)`: `0.7032`
- `categorical__program_description_Arch Tech: Design 2`: `0.6970`
- `categorical__program_code_1_AS_ARDD`: `0.6970`

## Top Negative Coefficients

- `categorical__ethnicity_detail_Asian - Cambodian`: `-1.3300`
- `categorical__residency_Foreign`: `-1.0945`
- `categorical__education_goal_Complete credits for GED/HS`: `-0.8938`
- `categorical__education_goal_Improve basic skills`: `-0.8294`
- `categorical__program_description_Interior Design: Merchandising`: `-0.6913`
- `categorical__program_code_1_CN_IDIM`: `-0.6913`
- `categorical__program_description_Entrepreneurship`: `-0.6733`
- `categorical__program_code_1_CE_BAEN`: `-0.6733`
- `categorical__ipeds_ethnicity_Pacific Islander`: `-0.6544`
- `categorical__program_description_Real Estate Broker`: `-0.6443`
