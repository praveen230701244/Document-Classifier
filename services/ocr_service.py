from __future__ import annotations

from pathlib import Path
import cv2
import pytesseract

# ✅ Correct Tesseract path (your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\prave\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

from utils.image_processing import preprocess_for_ocr


class OCRServiceError(Exception):
    pass


def process_image_and_extract_text(image_path: Path, processed_folder: Path) -> dict[str, str]:
    
    # Load image
    image = cv2.imread(str(image_path))
    if image is None:
        raise OCRServiceError("Could not load image for OCR.")

    # Preprocess image
    processed = preprocess_for_ocr(image)

    # Save processed image
    processed_folder.mkdir(parents=True, exist_ok=True)
    processed_path = processed_folder / image_path.name
    cv2.imwrite(str(processed_path), processed)

    try:
        # Perform OCR
        text = pytesseract.image_to_string(processed, config="--oem 3 --psm 6")

    except pytesseract.TesseractNotFoundError as exc:
        raise OCRServiceError(
            "Tesseract is not installed or not found. Check installation path."
        ) from exc

    except Exception as exc:
        raise OCRServiceError(f"OCR engine failed: {exc}") from exc

    # Clean result
    text = text.strip()

    if not text:
        raise OCRServiceError("No readable text detected in the document.")

    return {
        "text": text,
        "processed_path": str(processed_path)
    }