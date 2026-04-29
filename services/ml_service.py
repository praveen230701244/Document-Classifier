from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any

from model.train import train_and_save_model

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "model" / "vectorizer.pkl"

_MODEL: Any = None
_VECTORIZER: Any = None


def bootstrap_model() -> None:
    global _MODEL, _VECTORIZER
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        train_and_save_model()

    with open(MODEL_PATH, "rb") as model_file:
        _MODEL = pickle.load(model_file)
    with open(VECTORIZER_PATH, "rb") as vectorizer_file:
        _VECTORIZER = pickle.load(vectorizer_file)


def classify_document(cleaned_text: str) -> dict[str, Any]:
    if _MODEL is None or _VECTORIZER is None:
        bootstrap_model()

    vector = _VECTORIZER.transform([cleaned_text])
    label = _MODEL.predict(vector)[0]
    probabilities = _MODEL.predict_proba(vector)[0]
    confidence = float(probabilities.max()) * 100

    return {"label": label, "confidence": round(confidence, 2)}
