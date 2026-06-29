# Roof Imoveis - Housing Price Analysis

This repository contains the original housing-price notebook and a new lightweight Python profiling layer under `src/roof_imoveis/`.

## What this PR changes

The notebook remains the source of the full EDA and modeling workflow. The Python code added here is an engineering foundation, not a full rewrite of the notebook. It provides:

- local CSV/Excel ingestion with explicit errors;
- normalized column names;
- missing-value and numeric profiling outputs;
- duplicate-row metrics;
- an optional `price_summary.csv` when the dataset includes the `price` column;
- tests for ingestion and profiling behavior.

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
├── tests/
├── requirements.txt
└── README.md
```

## Dataset requirement

This repository already contains `kc_house_data.csv` at the root. For a cleaner project layout, future runs can copy it to `data/raw/kc_house_data.csv`, but the current command below uses the existing root file.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m pytest
python -m roof_imoveis.pipeline --input kc_house_data.csv --output data/processed
```

On Linux/macOS, use `source .venv/bin/activate`.

## Outputs

Always generated when the input file exists:

- `data/processed/missing_summary.csv`
- `data/processed/numeric_summary.csv`
- `data/processed/dataset_metrics.json`

Generated only when the expected housing column exists:

- `data/processed/price_summary.csv`

## Current limitations

- Model training still lives in the notebook.
- This PR does not add a production-grade training pipeline.
- Data contracts for expected columns and valid ranges still need to be formalized.
- Notebook metrics should be exported to reproducible reports in future work.
