# Project Agent Notes

## Purpose

This file is the running project memory for the logistic regression study. It tracks what we have decided, what is still open, and what we should do next. It should be updated as the project evolves.

## Project Summary

- Project: logistic regression study on student academic outcomes
- Cohort structure: students grouped by fall-entry cohort
- Current stage: planning and study design

## Current Artifacts

- [logistic_regression_study_plan.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/logistic_regression_study_plan.md): initial planning document for the study
- [README.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/README.md): project setup and starter commands
- [data_dictionary.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/data_dictionary.md): first-pass variable roles and modeling notes
- [outputs/raw_data_profile.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/raw_data_profile.md): summary of the raw workbook structure and distributions
- [data/processed/cohort_model_dataset.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/data/processed/cohort_model_dataset.csv): cleaned modeling dataset
- [data/processed/primary_analysis_cohort.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/data/processed/primary_analysis_cohort.csv): filtered primary study cohort
- [outputs/primary_analysis_cohort.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/primary_analysis_cohort.md): summary of the primary cohort inclusion rules
- [outputs/degree_obtained_model_report.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/degree_obtained_model_report.md): baseline logistic model results using `degree_obtained`
- [outputs/degree_obtained_model_coefficients.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/degree_obtained_model_coefficients.csv): baseline model coefficients
- [outputs/primary_degree_obtained_model_report.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/primary_degree_obtained_model_report.md): baseline model results for the primary filtered cohort
- [outputs/primary_degree_obtained_model_coefficients.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/primary_degree_obtained_model_coefficients.csv): coefficients for the primary filtered cohort model
- [outputs/refined_primary_degree_obtained_model_report.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/refined_primary_degree_obtained_model_report.md): refined baseline model using a reduced predictor set
- [outputs/refined_primary_degree_obtained_model_coefficients.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/refined_primary_degree_obtained_model_coefficients.csv): coefficients for the refined baseline model
- [data/processed/interpretive_primary_analysis_cohort.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/data/processed/interpretive_primary_analysis_cohort.csv): grouped version of the primary cohort for interpretive modeling
- [outputs/interpretive_dataset_summary.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/interpretive_dataset_summary.md): grouped-category summary for the interpretive dataset
- [outputs/statsmodels_degree_obtained_report.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/statsmodels_degree_obtained_report.md): statsmodels logistic regression report with odds ratios and p-values
- [outputs/statsmodels_degree_obtained_coefficients.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/statsmodels_degree_obtained_coefficients.csv): coefficient table for the statsmodels model
- [outputs/methods_summary.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/methods_summary.md): concise summary of the current official cohort and model specification
- [outputs/stakeholder_findings_summary.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/stakeholder_findings_summary.md): plain-language summary of the current main findings
- [outputs/html/stakeholder_findings_summary.html](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/html/stakeholder_findings_summary.html): browser-friendly HTML version of the stakeholder summary
- [outputs/html/methods_summary.html](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/html/methods_summary.html): browser-friendly HTML version of the methods summary
- [outputs/html/statsmodels_degree_obtained_report.html](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/outputs/html/statsmodels_degree_obtained_report.html): browser-friendly HTML version of the statsmodels report
- [scripts/run_full_pipeline.py](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/scripts/run_full_pipeline.py): single-command pipeline runner for local use or notebook environments like Colab
- [notebooks/degree_attainment_google_colab.ipynb](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/notebooks/degree_attainment_google_colab.ipynb): Colab-ready notebook template for collaborators
- [scripts/score_at_risk_students.py](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/scripts/score_at_risk_students.py): student-level risk scoring script for outreach lists
- [scripts/train_validated_outreach_model.py](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/scripts/train_validated_outreach_model.py): validated train/test outreach model for risk ranking
- [scripts/run_multi_college_pipeline.py](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/scripts/run_multi_college_pipeline.py): configurable pipeline runner for sister colleges
- [templates/column_mapping.example.json](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/column_mapping.example.json): example raw-to-standard column mapping
- [templates/college_config.example.json](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/college_config.example.json): example college-specific cohort and modeling configuration
- [multi_cohort_dataset_schema.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/multi_cohort_dataset_schema.md): recommended schema for a combined multi-cohort 3-year completion dataset
- [templates/multi_cohort_data_request_template.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/multi_cohort_data_request_template.md): reusable request template for gathering cohort data
- [templates/multi_cohort_completion_dataset_template.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/multi_cohort_completion_dataset_template.csv): blank CSV template with the recommended combined dataset headers

## Working Objective

Build a clear, reusable framework for analyzing a binary student academic outcome using logistic regression across fall cohorts.

## Decisions Made

- We created an initial planning document for the study.
- The study is currently framed around fall-entry cohorts.
- The analysis will use logistic regression, which means the primary modeled outcome must be binary.
- Python is the recommended implementation language for the project.
- The initial project structure will use separate folders for raw data, processed data, notebooks, reusable code, scripts, and outputs.
- A project-local Python virtual environment was created in `.venv`.
- The current raw file is `cohort.xlsx`.
- The current raw file contains one fall cohort only: `Term_Code = 202170`.
- The current raw file contains 3,613 student rows and 25 columns.
- `Degree_obtained` is available as a binary candidate outcome in the current file.
- `Degree_obtained` is now confirmed as the primary study outcome.
- In this project, `Degree_obtained = 1` means the student completed within the Fall 2021 to Spring 2024 three-academic-year window.
- `WD` in `attendance_status` means non-credit students.
- The first baseline model was run using `degree_obtained` as the outcome.
- The baseline model achieved roughly 0.700 ROC AUC on the holdout split.
- The primary analysis cohort will exclude `WD` and restrict to degree, certificate, and transfer-oriented education goals.
- The primary filtered cohort contains 3,140 students.
- The first filtered-cohort model achieved roughly 0.682 ROC AUC on the holdout split.
- The refined reduced-feature model achieved roughly 0.705 ROC AUC on the holdout split.
- The grouped statsmodels model achieved roughly 0.719 ROC AUC on the full primary cohort.
- The grouped statsmodels model is the current best interpretive model for reporting.
- A plain-language stakeholder findings summary has been created from the current statsmodels results.
- HTML exports now exist for the main summary reports.
- A Colab-friendly notebook and a one-command full pipeline runner now exist for collaborators.
- A student-level at-risk scoring step now exists for support/outreach use.
- A validated train/test outreach model now exists and is the preferred operational scoring path.
- A reusable multi-college template now exists so sister colleges can retrain the same methodology on their own data.
- A concrete multi-cohort schema and data-request template now exist for assembling additional cohorts.
- The multi-cohort schema now distinguishes raw award/history tables from the student-level modeling table.
- The multi-cohort schema now supports multiple awards per student and derived English/math first-success indicators.

## Open Questions

- What exact outcome will be modeled first?
- Which additional fall cohort years should be included for multi-cohort analysis?
- Which student populations should be included or excluded?
- What data sources are available for predictors and outcomes?
- Will we run one pooled model, separate cohort models, or both?
- Should high-cardinality features like program and zipcode be reduced, grouped, or filtered before the primary model?

## Assumptions

- The project is still in the planning phase.
- No finalized dataset has been provided yet.
- The study may eventually require a data dictionary, analytic dataset specification, and modeling workflow.

## Immediate Next Steps

1. Decide whether the top-10% / next-20% outreach tier rule matches advisor capacity.
2. Review whether the current grouped categories and cohort rules should become district-wide template defaults.
3. Determine whether more fall cohorts will be added before final modeling.
4. Decide whether to add interaction terms such as attendance status by education goal.
5. If needed, add calibration plots and threshold-analysis outputs for the validated outreach model.

## Update Log

### 2026-05-05

- Created `logistic_regression_study_plan.md`.
- Created `agent.md` to serve as the running memory file for the project.
- Created the project folder scaffold for a Python workflow.
- Added `README.md` with the recommended build approach.
- Added `requirements.txt` with the initial Python package list.
- Added the raw data file `data/raw/cohort.xlsx`.
- Created `.venv` and installed the core Python analysis packages.
- Inspected the first workbook and confirmed it contains one fall cohort with unique student rows.
- Added starter scripts for raw data profiling and cleaned dataset creation.
- Ran the profiling script and created `outputs/raw_data_profile.md`.
- Ran the cleaning script and created `data/processed/cohort_model_dataset.csv`.
- Added and ran a baseline logistic model script using `degree_obtained`.
- Confirmed `degree_obtained` as the official primary outcome.
- Documented that `WD` means non-credit students.
- Added `data_dictionary.md` with the first-pass variable map and modeling notes.
- Added and ran the primary cohort filter for credit students with degree/certificate/transfer-oriented goals.
- Added and ran a filtered-cohort logistic model for the primary study population.
- Added support for custom feature exclusions in the training script.
- Ran a refined primary-cohort model excluding high-cardinality and sparse fields.
- Built a grouped interpretive dataset for stable category-level reporting.
- Fit a statsmodels logistic regression and produced odds ratios, confidence intervals, and p-values.
- Added a concise methods summary for the current official model.
- Added a plain-language stakeholder findings summary.
- Added a reusable Markdown-to-HTML export script and generated HTML report versions.
- Added a Colab-ready notebook and a reusable end-to-end pipeline runner.
- Verified the full pipeline runner against the current cohort file.
- Added and ran a student-level at-risk scoring script.
- Added and ran a validated train/test outreach model with a safer default feature set.
- Updated the full pipeline runner to produce validated outreach scoring outputs.
- Added a configurable multi-college runner plus example mapping and college config files.
- Verified the multi-college runner against the current cohort file and example configs.
- Added a formal multi-cohort dataset schema and data-request template.
- Expanded the schema/template to support award-level source data, student-level rollups, and English/math first-success fields.

## Update Rule

Each time we make progress, this file should be updated with:

- new decisions
- added artifacts
- changed assumptions
- outstanding blockers
- next recommended action
