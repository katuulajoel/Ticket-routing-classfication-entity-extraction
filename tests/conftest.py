"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DATA = ROOT / "data"

sys.path.insert(0, str(SRC))


@pytest.fixture
def ticket_dataframe() -> pd.DataFrame:
    from src.data_loader import load_ticket_data

    return load_ticket_data(DATA / "tickets.csv")


@pytest.fixture
def sample_messages() -> list[str]:
    return [
        "Password reset not working for John Smith. Reach me at john.smith@example.com.",
        "Charged twice on my invoice. Please call (555) 123-4567.",
        "Your mobile app crashes when uploading a CSV file.",
    ]

