# Logistic Model Report

- Outcome: `degree_obtained`
- Rows used: `3,140`
- Train rows: `2,512`
- Test rows: `628`
- Positive rate: `0.340`
- Accuracy: `0.680`
- ROC AUC: `0.682`

## Dropped Columns

- `degree`
- `student_id`
- `student_type`
- `term_code`
- `term_semester`

## Top Positive Coefficients

- `categorical__program_code_1_CN_AMAV`: `0.7882`
- `categorical__program_description_Avionics`: `0.7882`
- `categorical__program_code_1_CT_DNDI`: `0.7785`
- `categorical__program_description_Dance Instructor`: `0.7785`
- `categorical__ethnicity_detail_Asian - Japanese`: `0.7624`
- `categorical__program_description_Immersive Media (VR/AR)`: `0.7387`
- `categorical__program_code_1_CT_VRAR`: `0.7387`
- `categorical__program_code_1_CN_FTV`: `0.7280`
- `categorical__residency_VACA Non-Resident Fee Exemptn`: `0.7267`
- `categorical__program_code_1_CN_PILA`: `0.6829`

## Top Negative Coefficients

- `categorical__ethnicity_detail_Asian - Cambodian`: `-1.1300`
- `categorical__residency_Foreign`: `-0.8265`
- `categorical__attendance_status_PT`: `-0.7342`
- `categorical__program_description_Computer Information Systems`: `-0.7138`
- `categorical__program_description_Culinary Arts Basic`: `-0.6558`
- `categorical__program_code_1_CT_CAAP`: `-0.6558`
- `categorical__program_code_1_CE_AVCP`: `-0.6309`
- `categorical__program_description_Aviation Sci: Commercial Pilot`: `-0.6309`
- `categorical__ipeds_ethnicity_Pacific Islander`: `-0.6231`
- `categorical__program_description_Accounting`: `-0.6207`
