"""Tests for ticket data loading utilities."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.data_loader import ensure_required_columns, load_ticket_data


def test_load_ticket_data_success(tmp_path: Path) -> None:
    """Loading a valid CSV returns cleaned records."""

    csv_path = tmp_path / "tickets.csv"
    df = pd.DataFrame(
        {
            "ticket_id": [1, 2],
            "message": ["  Password reset not working  ", "Billing issue"],
            "category": ["authentication", "billing"],
        }
    )
    df.to_csv(csv_path, index=False)

    loaded = load_ticket_data(csv_path)
    assert set(loaded.columns) >= {"ticket_id", "message", "category"}
    assert "Password reset not working" in loaded["message"].tolist()


def test_ensure_required_columns_missing() -> None:
    """Validates required schema enforcement."""

    df = pd.DataFrame({"ticket_id": [1], "message": ["Hello"]})
    with pytest.raises(ValueError, match="Missing required columns"):
        ensure_required_columns(df, {"ticket_id", "message", "category"})


def test_load_ticket_data_empty_after_cleaning(tmp_path: Path) -> None:
    """Empty content after cleaning triggers a helpful error."""

    csv_path = tmp_path / "tickets.csv"
    df = pd.DataFrame(
        {
            "ticket_id": [1],
            "message": ["   "],
            "category": ["billing"],
        }
    )
    df.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="empty after cleaning"):
        load_ticket_data(csv_path)


def test_load_ticket_data_integration_dataset() -> None:
    """Validate real dataset size and category coverage."""

    df = load_ticket_data(Path("data/tickets.csv"))

    assert len(df) == 100
    assert set(df["category"]) == {"authentication", "billing", "technical", "product", "account"}
