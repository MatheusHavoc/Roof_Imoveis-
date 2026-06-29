# Roof Imoveis - Housing Price Analysis

Professional Python project for housing price analysis using the King County house sales dataset. The original notebook is preserved, and reusable pipeline code was added under `src/`.

## Staff Data Engineer assessment

This is currently the strongest portfolio repository. It contains a real dataset, quality checks, exploratory analysis and predictive modeling. The main improvement needed was engineering structure: packaging reusable logic, documenting execution and adding tests.

## Repository structure

```text
.
├── Roof_Imóveis_2.ipynb
├── kc_house_data.csv
├── data/
│   ├── raw/
│   └── processed/
├── images/
├── notebooks/
├── src/roof_imoveis/
│   ├── __init__.py
│   └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
python -m roof_imoveis.pipeline --input kc_house_data.csv --output data/processed
```

On Linux/macOS, use `source .venv/bin/activate`.

## What the Python pipeline does

- Loads CSV or Excel data with explicit error handling.
- Normalizes column names for downstream processing.
- Produces missing-value summaries.
- Produces numeric descriptive statistics.
- Produces duplicate-row metrics.
- Writes artifacts to `data/processed/`.

## Current limitations

- The richest modeling workflow still lives in the notebook.
- Model training should be moved into a dedicated `modeling.py` module in a later PR.
- The project should add data contracts for expected columns and value ranges.
- Metrics from the notebook should be exported into reproducible reports.
