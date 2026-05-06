# Stakeholder Findings Summary

## Overview

This summary highlights the current findings from the logistic regression study of `degree_obtained` for the current fall-entry cohort.

The current primary analysis focuses on:

- credit students only (`FT` or `PT`)
- students with degree-, certificate-, or transfer-oriented education goals
- one fall cohort (`Term_Code = 202170`)

The current analysis includes `3,140` students.

## Model Context

- Outcome: `degree_obtained`
- Model type: logistic regression
- Overall model performance: `0.719` ROC AUC
- Interpretation note: these results show associations, not causal effects

## Key Findings

- Full-time students had much higher odds of degree attainment than part-time students.
  Odds ratio: `3.26`
  95% CI: `(2.68, 3.96)`

- Students identified as Asian had higher odds of degree attainment than students identified as Hispanic, after controlling for the other variables in the model.
  Odds ratio: `1.81`
  95% CI: `(1.45, 2.25)`

- Students identified as White also had higher odds of degree attainment than students identified as Hispanic.
  Odds ratio: `1.40`
  95% CI: `(1.13, 1.72)`

- Male students had lower odds of degree attainment than female students.
  Odds ratio: `0.68`
  95% CI: `(0.58, 0.80)`

- Students who were BOG-eligible had higher odds of degree attainment than students who were not BOG-eligible.
  Odds ratio: `1.54`
  95% CI: `(1.27, 1.87)`

- Students from feeder high schools had higher odds of degree attainment than students from non-feeder high schools.
  Odds ratio: `1.42`
  95% CI: `(1.13, 1.78)`

- Students whose education goal was associate degree only had lower odds of degree attainment than students with transfer-oriented goals.
  Odds ratio: `0.61`
  95% CI: `(0.41, 0.90)`

## Findings To Treat Carefully

- International students showed higher estimated odds of degree attainment, but the confidence interval was wide, which suggests more uncertainty.
  Odds ratio: `4.53`
  95% CI: `(1.42, 14.41)`

- Students with recorded disabilities showed higher estimated odds of degree attainment in this model, but this should be interpreted carefully and in institutional context.
  Odds ratio: `1.57`
  95% CI: `(1.07, 2.30)`

- Age showed a slight negative relationship with degree attainment, but it was borderline rather than strongly conclusive in this model.
  Odds ratio per year: `0.97`
  95% CI: `(0.94, 1.00)`

## Variables That Were Not Strongly Distinguishing In This Version

- district status
- athlete status
- certificate or vocational goal compared with transfer-oriented goal
- grouped “other” ethnicity category
- grouped “other/unknown” gender category

## Practical Interpretation

- Enrollment intensity appears to matter a great deal in this cohort. Full-time students had the strongest positive association with degree attainment.
- Goal alignment also matters. Students with transfer-oriented goals performed better than students whose goal was associate degree only.
- Some student background variables remain associated with the outcome even after controlling for other factors, which may help identify where support strategies should be explored further.

## Important Limits

- This analysis currently uses one cohort only.
- The model is based on available administrative variables, not every possible factor affecting student outcomes.
- Some categories were grouped to improve stability and interpretability.
- Results should be used for planning and inquiry, not for high-stakes individual decisions.

## Recommended Next Uses

- Use this summary as the basis for an initial stakeholder discussion.
- Review whether the grouped categories match institutional language and reporting standards.
- Expand the dataset to additional fall cohorts if cross-cohort comparison is still a project goal.
- Consider translating the strongest findings into intervention questions, especially around full-time/part-time differences and declared education goals.
