"""Tests for the EntityExtractor regex helper."""

from __future__ import annotations

from pathlib import Path

from src.data_loader import load_ticket_data
from src.entity_extractor import EntityExtractor


def test_extract_basic_entities(sample_messages: list[str]) -> None:
    """Recognizes person and email entities."""

    extractor = EntityExtractor()
    entities = extractor.extract(sample_messages[0])

    assert "PERSON" in entities
    assert any(match.text == "John Smith" for match in entities["PERSON"])
    assert "EMAIL" in entities


def test_annotate_phone_numbers(sample_messages: list[str]) -> None:
    """Phone number annotation inserts inline tags."""

    extractor = EntityExtractor()
    annotated = extractor.annotate(sample_messages[1])
    assert "|PHONE]" in annotated


def test_annotation_handles_multiple_types() -> None:
    """Multiple entity types remain intact in annotation."""

    extractor = EntityExtractor()
    text = "Contact Sarah Johnson at sarah@example.com about $129.50 invoice"
    annotated = extractor.annotate(text)

    assert "|PERSON]" in annotated
    assert "|EMAIL]" in annotated
    assert "|MONEY]" in annotated


def test_extract_entities_from_dataset_samples() -> None:
    """Dataset rows with known entities are parsed correctly."""

    df = load_ticket_data(Path("data/tickets.csv"))
    extractor = EntityExtractor()

    cases = {
        32: {"EMAIL": {"maria.g@example.com"}},
        40: {"EMAIL": {"finance@acme.org"}},
        28: {"MONEY": {"$1,200"}},
    }

    for ticket_id, expectations in cases.items():
        row = df.loc[df["ticket_id"] == ticket_id].iloc[0]
        entities = extractor.extract(row["message"])

        for entity_type, expected_texts in expectations.items():
            matches = {entity.text for entity in entities.get(entity_type, [])}
            assert expected_texts.issubset(matches), (
                f"Ticket {ticket_id} missing {entity_type} {expected_texts}"
            )

