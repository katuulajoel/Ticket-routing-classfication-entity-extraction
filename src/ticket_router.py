"""Module 2: Ticket routing model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


@dataclass
class PredictionResult:
    """Structured response for ticket routing predictions."""

    queue: str
    confidence: float


class TicketRouter:
    """Trainable text classification pipeline with confidence fallback."""

    def __init__(self, *, threshold: float = 0.55) -> None:
        """
        Initialize the router.

        Args:
            threshold: Minimum confidence required to auto-route tickets.
        """

        self.threshold = threshold
        self.model = None
        self.vectorizer = None

    def fit(self, texts: Iterable[str], labels: Iterable[str]) -> None:
        """Train the router on past ticket messages and categories."""
        texts_list = list(texts)
        labels_list = list(labels)
        
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(texts_list)
        
        self.model = LogisticRegression()
        self.model.fit(X, labels_list)

    def predict_with_confidence(self, texts: Iterable[str]) -> List[PredictionResult]:
        """Predict ticket queues with associated confidence scores."""
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Model has not been trained. Call fit() first.")
        
        texts_list = list(texts)
        X = self.vectorizer.transform(texts_list)
        
        probabilities = self.model.predict_proba(X)
        predictions = self.model.predict(X)
        
        results = []
        for pred, probs in zip(predictions, probabilities):
            max_prob = max(probs)
            results.append(self._format_prediction(pred, max_prob))
        
        return results

    def _format_prediction(self, label: str, probability: float) -> PredictionResult:
        """Apply thresholding logic to produce prediction results."""
        if probability < self.threshold:
            return PredictionResult(queue="manual_review", confidence=probability)
        return PredictionResult(queue=label, confidence=probability)

