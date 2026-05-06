# Logistic Regression Project

This project is being set up to support a logistic regression study on student academic outcomes by fall-entry cohort.

## Why Python

Python is a strong choice for this project because it gives us a practical workflow for:

- data cleaning with `pandas`
- exploratory analysis and plots
- logistic regression modeling
- validation and reproducibility
- exporting tables and results for reporting

If you later need more statistics-first output, we can also use `statsmodels` inside the same Python workflow.

## Recommended Python Stack

- `pandas` for data preparation
- `numpy` for numeric operations
- `jupyter` for exploration
- `scikit-learn` for train/test workflows and evaluation
- `statsmodels` for interpretable regression output like coefficients, odds ratios, and p-values
- `matplotlib` and `seaborn` for charts

## Local Environment

This project now includes a local virtual environment in `.venv`.

Use it with:

```bash
source .venv/bin/activate
```

## Starter Commands

## Google Colab Option

If someone wants to run the workflow in Google Colab instead of locally, use:

- [notebooks/degree_attainment_google_colab.ipynb](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/notebooks/degree_attainment_google_colab.ipynb)
- [scripts/run_full_pipeline.py](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/scripts/run_full_pipeline.py)

The notebook is the easiest option for collaborators. It lets them:

1. upload the raw Excel file
2. run the cleaning and cohort filters
3. fit the statsmodels logistic regression
4. download the processed cohort and coefficient table

The runner script is useful when someone wants a single command in Colab or another notebook environment after the file is uploaded.

## Multi-College Template

If sister colleges want to use the same methodology with their own data, use:

- [scripts/run_multi_college_pipeline.py](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/scripts/run_multi_college_pipeline.py)
- [templates/column_mapping.example.json](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/column_mapping.example.json)
- [templates/college_config.example.json](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/college_config.example.json)
- [multi_cohort_dataset_schema.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/multi_cohort_dataset_schema.md)
- [templates/multi_cohort_data_request_template.md](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/multi_cohort_data_request_template.md)
- [templates/multi_cohort_completion_dataset_template.csv](/Users/courtneyyoungberg/Desktop/Logistic%20Regression/templates/multi_cohort_completion_dataset_template.csv)

The multi-cohort materials now explicitly support:

- separate raw award/history tables
- student-level rolled-up modeling datasets
- multiple awards per student
- first-success term fields for English and math, plus derived early-success flags

Recommended setup for another college:

1. copy the example mapping file and map their raw columns to the standard cleaned names
2. copy the example college config and update included goals, groupings, and outreach features
3. run the pipeline on that college's own dataset
4. retrain and validate locally rather than reusing our coefficients

Profile the raw workbook:

```bash
./.venv/bin/python scripts/profile_raw_data.py --input data/raw/cohort.xlsx --output outputs/raw_data_profile.md
```

Build a cleaned modeling dataset:

```bash
./.venv/bin/python scripts/prepare_model_dataset.py --input data/raw/cohort.xlsx --output data/processed/cohort_model_dataset.csv
```

Build the primary analysis cohort:

```bash
./.venv/bin/python scripts/build_primary_analysis_cohort.py --input data/processed/cohort_model_dataset.csv --output data/processed/primary_analysis_cohort.csv --summary outputs/primary_analysis_cohort.md
```

Build the grouped interpretive dataset:

```bash
./.venv/bin/python scripts/build_interpretive_dataset.py --input data/processed/primary_analysis_cohort.csv --output data/processed/interpretive_primary_analysis_cohort.csv --summary outputs/interpretive_dataset_summary.md
```

Fit the stats-focused logistic model:

```bash
./.venv/bin/python scripts/train_statsmodels_logit.py --input data/processed/interpretive_primary_analysis_cohort.csv --report outputs/statsmodels_degree_obtained_report.md --coefficients outputs/statsmodels_degree_obtained_coefficients.csv
```

Score students for outreach risk tiers:

```bash
./.venv/bin/python scripts/score_at_risk_students.py --input data/processed/interpretive_primary_analysis_cohort.csv --output outputs/scored_primary_analysis_cohort.csv --summary outputs/at_risk_scoring_summary.md
```

Train a validated outreach model with a train/test split:

```bash
./.venv/bin/python scripts/train_validated_outreach_model.py --input data/processed/interpretive_primary_analysis_cohort.csv --output outputs/validated_scored_primary_analysis_cohort.csv --report outputs/validated_outreach_risk_model.md
```

Export Markdown summaries to HTML:

```bash
./.venv/bin/python scripts/export_markdown_to_html.py --input outputs/stakeholder_findings_summary.md outputs/methods_summary.md outputs/statsmodels_degree_obtained_report.md --output-dir outputs/html
```

Run the full pipeline end to end:

```bash
./.venv/bin/python scripts/run_full_pipeline.py --input data/raw/cohort.xlsx --output-dir pipeline_run
```

Run the reusable multi-college pipeline:

```bash
./.venv/bin/python scripts/run_multi_college_pipeline.py --input data/raw/cohort.xlsx --mapping-config templates/column_mapping.example.json --college-config templates/college_config.example.json --output-dir multi_college_run --college-name "Example College"
```

The full pipeline now also writes:

- `data/scored_primary_analysis_cohort.csv`
- `data/validated_scored_primary_analysis_cohort.csv`
- student-level predicted degree probability
- risk of non-completion
- risk percentile
- risk tier (`High`, `Medium`, `Low`)

## Recommended Use

Use the project in two modes:

- `Interpretive model`: the `statsmodels` workflow for odds ratios, confidence intervals, and reporting
- `Operational outreach model`: the validated train/test workflow for ranking students by risk and prioritizing extra support

The validated outreach model currently uses a safer default feature set that excludes grouped gender, ethnicity, residency, disability, and international-student status.

## Project Layout

- `data/raw/`: original source files
- `data/processed/`: cleaned analysis-ready datasets
- `notebooks/`: exploratory notebooks
- `src/`: reusable Python code
- `scripts/`: runnable data prep or modeling scripts
- `outputs/`: tables, charts, and model results

## Suggested Build Sequence

1. Receive and inspect the raw data.
2. Create a data dictionary and confirm the outcome variable.
3. Build a cleaned student-cohort dataset.
4. Run descriptive analysis and missingness checks.
5. Fit the first logistic regression model.
6. Evaluate model quality and interpret the results.
7. Refine and document the final workflow.

## When Your Data Is Ready

Once the data arrives, the first thing we should do is map each column into one of these groups:

- identifier fields
- cohort fields
- outcome field
- predictors known at entry
- predictors from first term or first year
- fields to exclude from modeling

At that point I can help you build the actual data prep and modeling code.
