"""Module 1: Data loading helpers for ticket routing challenge."""

from pathlib import Path
from typing import Iterable, Union

import pandas as pd


REQUIRED_COLUMNS = {"ticket_id", "message", "category"}


def load_ticket_data(path: Union[Path, str]) -> pd.DataFrame:
    """
    Load the ticket dataset for the routing challenge.

    TODO:
    - Read the CSV from the provided path (raise `FileNotFoundError` if missing).
    - Validate required columns using `ensure_required_columns`.
    - Drop records missing `message` or `category` and normalize whitespace.
    - Raise `ValueError` if the resulting DataFrame is empty.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    df = pd.read_csv(path)
    ensure_required_columns(df, REQUIRED_COLUMNS)
    
    df = df.dropna(subset=["message", "category"])
    df["message"] = df["message"].str.strip()
    df["category"] = df["category"].str.strip()
    
    # Remove rows with empty messages after stripping whitespace
    df = df[df["message"] != ""]
    
    if df.empty:
        raise ValueError("DataFrame is empty after cleaning")
    
    return df


def ensure_required_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """
    Ensure the DataFrame contains a required set of columns.

    TODO:
    - Identify missing columns and raise `ValueError` if any are absent.
    - Return the original DataFrame when validation succeeds to enable chaining.
    """
    missing_columns = set(columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return df
