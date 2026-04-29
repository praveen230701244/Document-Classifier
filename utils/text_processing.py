from __future__ import annotations

import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def _ensure_nltk() -> None:
    try:
        stopwords.words("english")
    except LookupError:
        nltk.download("stopwords", quiet=True)


def normalize_text_for_model(raw_text: str) -> str:
    _ensure_nltk()
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))

    text = raw_text.lower()
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\b\d{5,}\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = [tok for tok in text.split() if tok not in stop_words and len(tok) > 2]
    stemmed = [stemmer.stem(tok) for tok in tokens]
    return " ".join(stemmed)
