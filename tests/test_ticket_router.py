"""Tests for the TicketRouter classifier."""

from __future__ import annotations

import pandas as pd
import pytest

from src.ticket_router import PredictionResult, TicketRouter


def test_router_basic_training(ticket_dataframe: pd.DataFrame) -> None:
    """Router can train and produce predictions."""

    router = TicketRouter()
    router.fit(ticket_dataframe["message"], ticket_dataframe["category"])

    results = router.predict_with_confidence(ticket_dataframe["message"].head(2))
    assert len(results) == 2
    for result in results:
        assert isinstance(result, PredictionResult)
        assert 0 <= result.confidence <= 1


def test_router_manual_review_threshold(ticket_dataframe: pd.DataFrame) -> None:
    """Very high threshold routes to manual review."""

    router = TicketRouter(threshold=0.99)
    router.fit(ticket_dataframe["message"], ticket_dataframe["category"])

    result = router.predict_with_confidence(pd.Series(["unknown issue about custom integration"]))[0]
    assert result.queue == "manual_review"


def test_router_requires_fit_before_predict(sample_messages: list[str]) -> None:
    """Predicting without training raises a helpful error."""

    router = TicketRouter()
    with pytest.raises(RuntimeError, match="has not been trained"):
        router.predict_with_confidence(sample_messages)


def test_router_threshold_logic(ticket_dataframe: pd.DataFrame) -> None:
    """Thresholding flips between routing and manual review."""

    router = TicketRouter(threshold=0.5)
    router.fit(ticket_dataframe["message"], ticket_dataframe["category"])

    formatted = [router._format_prediction("billing", 0.8), router._format_prediction("product", 0.2)]
    assert formatted[0].queue == "billing"
    assert formatted[1].queue == "manual_review"


def test_router_predicts_every_category(ticket_dataframe: pd.DataFrame) -> None:
    """Ensure coverage across all categories using real dataset."""

    router = TicketRouter(threshold=0.0)
    router.fit(ticket_dataframe["message"], ticket_dataframe["category"])

    representatives = (
        ticket_dataframe.groupby("category").first().reset_index()
    )

    predictions = router.predict_with_confidence(representatives["message"])
    predicted_labels = {prediction.queue for prediction in predictions}

    assert predicted_labels == set(representatives["category"])
