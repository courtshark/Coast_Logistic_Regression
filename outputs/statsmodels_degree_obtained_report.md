# Statsmodels Logistic Regression Report

- Outcome: `degree_obtained`
- Dataset: grouped primary analysis cohort
- Rows used: `3,140`
- Accuracy on full cohort: `0.689`
- ROC AUC on full cohort: `0.719`
- McFadden pseudo R-squared: `0.107`

## Model Formula

```
degree_obtained ~ age + attendance_status + gender_grouped + ethnicity_grouped +
residency_grouped + athlete + disability + international_student +
district_status + high_school_feeder + bog_eligible + education_goal_grouped
```

## Most Statistically Informative Terms

- `C(attendance_status, Treatment(reference='PT'))[T.FT]`: OR=`3.260`, 95% CI=`(2.685, 3.959)`, p=`0.0000`
- `C(ethnicity_grouped, Treatment(reference='Hispanic'))[T.Asian]`: OR=`1.809`, 95% CI=`(1.453, 2.253)`, p=`0.0000`
- `C(gender_grouped, Treatment(reference='F'))[T.M]`: OR=`0.678`, 95% CI=`(0.577, 0.797)`, p=`0.0000`
- `C(bog_eligible, Treatment(reference='No'))[T.Yes]`: OR=`1.540`, 95% CI=`(1.269, 1.868)`, p=`0.0000`
- `C(ethnicity_grouped, Treatment(reference='Hispanic'))[T.White]`: OR=`1.397`, 95% CI=`(1.131, 1.725)`, p=`0.0019`
- `C(high_school_feeder, Treatment(reference='Not a Feeder HS'))[T.Feeder HS]`: OR=`1.416`, 95% CI=`(1.125, 1.782)`, p=`0.0030`
- `C(high_school_feeder, Treatment(reference='Not a Feeder HS'))[T.Unknown]`: OR=`0.612`, 95% CI=`(0.427, 0.878)`, p=`0.0076`
- `international_student`: OR=`4.529`, 95% CI=`(1.424, 14.405)`, p=`0.0105`
- `C(education_goal_grouped, Treatment(reference='Transfer-Oriented'))[T.Associate Degree]`: OR=`0.608`, 95% CI=`(0.412, 0.898)`, p=`0.0124`
- `disability`: OR=`1.571`, 95% CI=`(1.071, 2.304)`, p=`0.0207`
- `age`: OR=`0.967`, 95% CI=`(0.935, 1.001)`, p=`0.0543`
- `C(residency_grouped, Treatment(reference='California Resident'))[T.Nonresident/Foreign]`: OR=`1.521`, 95% CI=`(0.978, 2.366)`, p=`0.0626`
- `C(ethnicity_grouped, Treatment(reference='Hispanic'))[T.Black]`: OR=`0.490`, 95% CI=`(0.220, 1.091)`, p=`0.0808`
- `athlete`: OR=`1.262`, 95% CI=`(0.935, 1.705)`, p=`0.1284`
- `C(district_status, Treatment(reference='In-District'))[T.Out-of-District]`: OR=`0.859`, 95% CI=`(0.694, 1.064)`, p=`0.1633`
