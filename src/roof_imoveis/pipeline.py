from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import pandas as pd

LOGGER = logging.getLogger(__name__)


class DataValidationError(ValueError):
    """Raised when the input dataset does not match the expected contract."""


@dataclass(frozen=True)
class ProjectConfig:
    """Configuration for the King County housing profiling pipeline."""

    project_name: str
    default_dataset: str
    target_column: str = "price"


CONFIG = ProjectConfig(
    project_name="King County housing price analysis",
    default_dataset="kc_house_data.csv",
)


def normalize_column_name(column: object) -> str:
    """Return a stable snake_case-like column name."""
    return str(column).strip().lower().replace(" ", "_").replace("-", "_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the dataframe with normalized columns."""
    cleaned = df.copy()
    cleaned.columns = [normalize_column_name(column) for column in cleaned.columns]
    return cleaned


def load_dataset(
    path: str | Path, required_columns: Sequence[str] = ()
) -> pd.DataFrame:
    """Load a CSV or Excel dataset and validate required columns."""
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    LOGGER.info("Loading dataset from %s", dataset_path)
    if dataset_path.suffix.lower() == ".csv":
        df = pd.read_csv(dataset_path)
    elif dataset_path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(dataset_path)
    else:
        raise DataValidationError(f"Unsupported file format: {dataset_path.suffix}")
    df = normalize_columns(df)
    missing = sorted(set(required_columns) - set(df.columns))
    if missing:
        raise DataValidationError(f"Missing required columns: {missing}")
    return df


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return null counts and percentages by column."""
    total_rows = len(df)
    summary = pd.DataFrame(
        {"column": df.columns, "missing_count": df.isna().sum().values}
    )
    summary["missing_pct"] = (
        0.0 if total_rows == 0 else summary["missing_count"] / total_rows
    )
    return summary.sort_values(
        ["missing_count", "column"], ascending=[False, True]
    ).reset_index(drop=True)


def duplicate_summary(df: pd.DataFrame) -> dict[str, int]:
    """Return row and duplicate counts."""
    return {"row_count": int(len(df)), "duplicate_rows": int(df.duplicated().sum())}


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for numeric columns."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.describe().transpose().reset_index(names="column")


def price_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return housing-price summaries when King County price columns are present."""
    if CONFIG.target_column not in df.columns:
        LOGGER.info(
            "Skipping price summary; missing optional column: %s", CONFIG.target_column
        )
        return pd.DataFrame()

    group_columns = [
        column for column in ("bedrooms", "bathrooms") if column in df.columns
    ]
    if not group_columns:
        return pd.DataFrame(
            {
                "metric": ["price_mean", "price_median"],
                "value": [
                    float(df[CONFIG.target_column].mean()),
                    float(df[CONFIG.target_column].median()),
                ],
            }
        )

    return (
        df.groupby(group_columns, dropna=False)
        .agg(
            records=(CONFIG.target_column, "size"),
            avg_price=(CONFIG.target_column, "mean"),
            median_price=(CONFIG.target_column, "median"),
        )
        .reset_index()
        .sort_values("records", ascending=False)
    )


def run_pipeline(
    input_path: str | Path, output_dir: str | Path = "data/processed"
) -> dict[str, Any]:
    """Run local profiling and optional housing-price summaries for an available dataset."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    df = load_dataset(input_path)
    missing = missing_summary(df)
    numeric = numeric_summary(df)
    duplicates = duplicate_summary(df)
    prices = price_summary(df)
    missing.to_csv(output_path / "missing_summary.csv", index=False)
    numeric.to_csv(output_path / "numeric_summary.csv", index=False)
    if not prices.empty:
        prices.to_csv(output_path / "price_summary.csv", index=False)
    (output_path / "dataset_metrics.json").write_text(
        json.dumps(duplicates, indent=2), encoding="utf-8"
    )
    LOGGER.info("Pipeline completed for %s", CONFIG.project_name)
    return {
        "rows": duplicates["row_count"],
        "duplicate_rows": duplicates["duplicate_rows"],
        "outputs": str(output_path),
    }


def build_parser() -> argparse.ArgumentParser:
    """Create CLI parser."""
    parser = argparse.ArgumentParser(description=CONFIG.project_name)
    parser.add_argument("--input", required=True, help="Path to raw CSV or Excel file.")
    parser.add_argument(
        "--output", default="data/processed", help="Directory for generated artifacts."
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entrypoint."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    args = build_parser().parse_args(argv)
    try:
        result = run_pipeline(args.input, args.output)
    except Exception:
        LOGGER.exception("Pipeline failed")
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
