# Logistic Regression Study Plan

## Study Purpose

This document outlines a logistic regression study to analyze student academic outcomes by fall-entry cohort. The goal is to identify which student, enrollment, and academic characteristics are associated with a defined outcome of interest and to support planning, intervention, and reporting.

## Core Research Question

For students grouped by each fall term cohort, which factors are associated with the probability of the selected academic outcome?

## Proposed Use Cases

- Estimate the likelihood of the outcome for students in each fall cohort.
- Identify significant predictors that can inform student support strategies.
- Compare model behavior across cohorts and over time.
- Produce a repeatable framework for future cohort analyses.

## Define the Outcome

The first planning decision is the dependent variable. Because logistic regression requires a binary outcome, choose one clear definition such as:

- `retained_next_fall`: student enrolled in the next fall term (`1=yes`, `0=no`)
- `completed_within_n_years`: student completed within a defined time window
- `good_academic_standing`: student remains in good standing after the first year
- `stop_out`: student stopped enrolling within a defined period

Only one primary outcome should be used per model. If multiple outcomes matter, treat them as separate analyses.

## Cohort Definition

Define cohorts consistently using the fall term as the entry point.

- Include all students whose first eligible term is a fall term.
- Create one cohort per fall term, for example `Fall 2018`, `Fall 2019`, `Fall 2020`, and so on.
- Decide whether transfer, first-time-in-college, graduate, or non-degree students should be included or excluded.
- Document whether students can appear in only one cohort or multiple analytic datasets.

## Unit of Analysis

The recommended unit of analysis is one row per student per fall-entry cohort.

Example keys:

- `student_id`
- `entry_fall_term`

## Candidate Predictor Variables

Predictors should be selected based on policy relevance, availability, and timing. Use variables known at or near cohort entry when possible.

### Demographic Variables

- age at entry
- gender
- race/ethnicity
- residency status
- first-generation indicator
- Pell eligibility

### Academic Preparation

- high school GPA
- placement level
- developmental education placement
- transfer units at entry
- admission category

### Enrollment Characteristics

- full-time/part-time status
- credit load in first term
- program or major at entry
- college/division
- modality if relevant

### Early Academic Performance

If the outcome occurs after the first term or first year, these may be appropriate:

- first-term GPA
- credits attempted
- credits earned
- completion ratio
- course withdrawal count
- probation indicator

### Support and Engagement Variables

- advising participation
- financial aid receipt
- learning support usage
- orientation completion

## Data Timing Rules

Each predictor must be available before the outcome window begins. This helps avoid leakage.

Examples:

- If modeling `retained_next_fall`, first-term and first-year variables may be acceptable if defined consistently.
- If modeling an outcome at the end of the first term, do not use post-term information.

## Analytic Dataset Structure

Recommended fields:

- `student_id`
- `entry_fall_term`
- outcome variable
- predictor fields
- exclusion flags
- missingness indicators where useful

Recommended preparation steps:

- remove duplicate student-cohort rows
- standardize categorical values
- encode missing values consistently
- winsorize or review implausible numeric outliers when justified
- create derived flags with documented logic

## Model Specification

Baseline model:

`logit(P(outcome=1)) = b0 + b1X1 + b2X2 + ... + bkXk`

Recommended approach:

- start with a theory-driven baseline model
- avoid adding highly overlapping predictors together without checking collinearity
- use reference groups intentionally for categorical variables
- consider separate models by student type if populations differ substantially

Possible extensions:

- one pooled model with cohort fixed effects
- separate model per cohort for comparison
- interaction terms such as cohort by full-time status if substantively justified

## Model Diagnostics and Validation

At minimum, assess:

- class balance
- missing data patterns
- multicollinearity
- coefficient direction and interpretability
- standard errors and confidence intervals

Performance checks:

- train/test split or cross-validation
- ROC-AUC
- precision, recall, and confusion matrix
- calibration review

If outcome classes are highly imbalanced, consider:

- threshold tuning
- class weights
- resampling only if methodologically justified

## Interpretation Plan

Primary outputs should include:

- odds ratios
- confidence intervals
- p-values
- marginal interpretation in plain language where useful

Example interpretation format:

- "Students enrolled part-time in their first fall term had lower odds of being retained to the next fall, holding other factors constant."

## Missing Data Strategy

Choose a documented rule before modeling:

- complete-case analysis if missingness is limited
- missing indicator approach for selected variables
- imputation if appropriate and supported

The choice should reflect missingness rate, mechanism, and stakeholder expectations.

## Inclusion and Exclusion Decisions

Document decisions explicitly, including:

- which student populations are excluded
- whether deceased or fully withdrawn students are handled separately
- how dual-enrolled or non-degree students are treated
- minimum data completeness requirements

## Governance and Ethics

- use only approved student-level data
- protect personally identifiable information
- restrict outputs to aggregated or authorized analytic views
- avoid using sensitive variables without a clear institutional reason
- frame results as associations, not proof of causation

## Deliverables

Recommended deliverables for the study:

- planning document
- data dictionary
- cohort definition document
- modeling codebook
- final analytic dataset specification
- results summary by cohort
- executive summary for stakeholders

## Recommended Workflow

1. Confirm the primary binary outcome.
2. Finalize cohort inclusion rules.
3. Inventory available data sources and variable definitions.
4. Build the student-cohort analytic dataset.
5. Perform descriptive analysis and missingness review.
6. Fit baseline logistic regression model.
7. Validate, refine, and document model decisions.
8. Prepare interpretation and reporting materials.

## Open Decisions To Finalize

- What exact academic outcome should be modeled?
- What cohort years should be included?
- Should the study focus on all students or a specific population?
- Will the analysis be pooled across cohorts or run separately by cohort?
- Which early academic variables are available and approved for use?

## Suggested Next Step

Once the outcome is confirmed, the next artifact to create should be a variable inventory table with:

- variable name
- definition
- source system
- timing relative to cohort entry
- data type
- expected coding
- inclusion decision
