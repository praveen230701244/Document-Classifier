from __future__ import annotations

import re


INVOICE_AMOUNT_PATTERN = re.compile(
    r"(?:total|amount|grand total|net payable)\s*[:\-]?\s*(?:rs\.?|inr|\$)?\s*([\d,]+(?:\.\d{1,2})?)",
    re.IGNORECASE,
)
INVOICE_DATE_PATTERN = re.compile(
    r"(?:date|invoice date)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
    re.IGNORECASE,
)
INVOICE_NUMBER_PATTERN = re.compile(
    r"(?:invoice\s*(?:no|number|#)|bill\s*no)\s*[:\-]?\s*([A-Z0-9\-\/]+)",
    re.IGNORECASE,
)

REPORT_HEADING_PATTERN = re.compile(
    r"(?im)^(?:\d+(?:\.\d+)*)?\s*(executive summary|introduction|methodology|analysis|findings|results|discussion|conclusion|recommendations)\b"
)

RESUME_SKILLS = [
    "python",
    "java",
    "sql",
    "machine learning",
    "data analysis",
    "deep learning",
    "flask",
    "react",
    "communication",
    "leadership",
    "aws",
    "docker",
    "nlp",
]
RESUME_EDUCATION_KEYWORDS = [
    "bachelor",
    "master",
    "phd",
    "university",
    "college",
    "degree",
    "cgpa",
    "gpa",
]


def extract_document_intelligence(doc_type: str, text: str) -> dict[str, list[str] | str]:
    lowered = text.lower()
    if doc_type == "invoice":
        amount = _single_match(INVOICE_AMOUNT_PATTERN, text)
        date = _single_match(INVOICE_DATE_PATTERN, text)
        invoice_number = _single_match(INVOICE_NUMBER_PATTERN, text)
        return {
            "invoice_number": invoice_number or "Not found",
            "date": date or "Not found",
            "amount": amount or "Not found",
        }

    if doc_type == "resume":
        found_skills = [skill for skill in RESUME_SKILLS if skill in lowered]
        education = [kw for kw in RESUME_EDUCATION_KEYWORDS if kw in lowered]
        return {
            "skills": found_skills if found_skills else ["Not found"],
            "education_keywords": education if education else ["Not found"],
        }

    if doc_type == "report":
        headings = REPORT_HEADING_PATTERN.findall(text)
        normalized = sorted({h.strip().title() for h in headings})
        return {"headings_or_sections": normalized if normalized else ["Not found"]}

    return {"note": "No extraction rule for predicted class."}


def _single_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()
