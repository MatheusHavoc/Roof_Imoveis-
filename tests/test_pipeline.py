from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from roof_imoveis.pipeline import load_dataset, missing_summary, run_pipeline


def test_load_dataset_normalizes_columns(tmp_path):
    dataset = tmp_path / "sample.csv"
    pd.DataFrame({"Sale Price": [100, None], "Zip Code": [1, 2]}).to_csv(
        dataset, index=False
    )
    df = load_dataset(dataset)
    assert list(df.columns) == ["sale_price", "zip_code"]


def test_missing_summary_counts_nulls():
    df = pd.DataFrame({"a": [1, None], "b": ["x", "y"]})
    summary = missing_summary(df)
    assert summary.loc[summary["column"] == "a", "missing_count"].iloc[0] == 1


def test_run_pipeline_writes_outputs(tmp_path):
    dataset = tmp_path / "sample.csv"
    output = tmp_path / "processed"
    pd.DataFrame({"price": [100, 200, 200]}).to_csv(dataset, index=False)
    result = run_pipeline(dataset, output)
    assert result["rows"] == 3
    assert (output / "missing_summary.csv").exists()
    assert (output / "numeric_summary.csv").exists()
    assert (output / "dataset_metrics.json").exists()
