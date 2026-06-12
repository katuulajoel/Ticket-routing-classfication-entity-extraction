"""Module 3: Rule-based entity extraction utilities."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, List, Tuple


@dataclass
class Entity:
    """Structured entity match."""

    text: str
    start: int
    end: int


class EntityExtractor:
    """Regex-based helper for extracting customer entities."""

    def __init__(self) -> None:
        self.patterns: Dict[str, List[re.Pattern[str]]] = {
            "PERSON": [
                re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"),
                re.compile(r"\bMr\. [A-Z][a-z]+\b"),
                re.compile(r"\bMs\. [A-Z][a-z]+\b"),
            ],
            "EMAIL": [
                re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
            ],
            "PHONE": [
                re.compile(r"\(\d{3}\)\s?\d{3}-\d{4}(?=\b|\D)"),
                re.compile(r"\d{3}-\d{3}-\d{4}(?=\b|\D)"),
            ],
            "MONEY": [
                re.compile(r"\$[\d,]+\.?\d*\b"),
            ],
        }

    def extract(self, text: str) -> Dict[str, List[Entity]]:
        """Extract entities from unstructured text."""
        results: Dict[str, List[Entity]] = {}
        
        for entity_type, patterns in self.patterns.items():
            entities: List[Entity] = []
            for pattern in patterns:
                for match in pattern.finditer(text):
                    entity = Entity(text=match.group(), start=match.start(), end=match.end())
                    entities.append(entity)
            if entities:
                results[entity_type] = entities
        
        return results

    def annotate(self, text: str) -> str:
        """Return text with inline entity annotations."""
        entities = self.extract(text)
        
        # Collect all entities with their positions and sort by start position (descending)
        all_entities: List[Tuple[int, int, str, str]] = []
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                all_entities.append((entity.start, entity.end, entity.text, entity_type))
        
        # Sort by start position descending to avoid offset issues when replacing
        all_entities.sort(key=lambda x: x[0], reverse=True)
        
        annotated_text = text
        for start, end, entity_text, entity_type in all_entities:
            annotation = f"[|{entity_type}]"
            annotated_text = annotated_text[:start] + annotation + annotated_text[end:]
        
        return annotated_text

