from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import (
    Blueprint,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.utils import secure_filename

from services.extraction_service import extract_document_intelligence
from services.ml_service import classify_document
from services.ocr_service import OCRServiceError, process_image_and_extract_text
from utils.text_processing import normalize_text_for_model

main_bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tif", "tiff"}
HISTORY: list[dict[str, Any]] = []
MAX_HISTORY = 30


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _ensure_directories() -> None:
    for key in ["UPLOAD_FOLDER", "PROCESSED_FOLDER", "RESULTS_FOLDER"]:
        Path(current_app.config[key]).mkdir(parents=True, exist_ok=True)


def _append_history(record: dict[str, Any]) -> None:
    HISTORY.insert(0, record)
    del HISTORY[MAX_HISTORY:]


@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", history=HISTORY[:10])


@main_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html", history=HISTORY)


@main_bp.route("/analyze", methods=["POST"])
def analyze_documents():
    _ensure_directories()
    files = request.files.getlist("documents")

    if not files:
        return render_template("index.html", history=HISTORY[:10], error="No files uploaded.")

    results: list[dict[str, Any]] = []
    for incoming_file in files:
        if incoming_file.filename == "":
            continue

        if not allowed_file(incoming_file.filename):
            logger.warning("Invalid file type for %s", incoming_file.filename)
            results.append(
                {
                    "filename": incoming_file.filename,
                    "status": "error",
                    "error": "Invalid file type. Upload images only.",
                }
            )
            continue

        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}_{secure_filename(incoming_file.filename)}"
        upload_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
        incoming_file.save(upload_path)
        logger.info("Upload accepted: %s", filename)

        try:
            ocr_result = process_image_and_extract_text(
                image_path=upload_path,
                processed_folder=Path(current_app.config["PROCESSED_FOLDER"]),
            )
            cleaned_text = normalize_text_for_model(ocr_result["text"])
            if not cleaned_text:
                raise OCRServiceError("OCR extracted empty or noisy text.")

            prediction = classify_document(cleaned_text)
            extracted_info = extract_document_intelligence(prediction["label"], ocr_result["text"])

            result_payload = {
                "filename": incoming_file.filename,
                "saved_filename": filename,
                "status": "success",
                "prediction": prediction["label"],
                "confidence": prediction["confidence"],
                "raw_text": ocr_result["text"],
                "processed_image_url": url_for("static", filename=f"uploads/processed/{filename}"),
                "original_image_url": url_for("static", filename=f"uploads/original/{filename}"),
                "extracted_info": extracted_info,
                "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            }

            json_filename = f"{Path(filename).stem}.json"
            json_path = Path(current_app.config["RESULTS_FOLDER"]) / json_filename
            json_path.write_text(json.dumps(result_payload, indent=2), encoding="utf-8")
            result_payload["json_download_url"] = url_for("static", filename=f"uploads/results/{json_filename}")
            results.append(result_payload)

            _append_history(
                {
                    "filename": incoming_file.filename,
                    "prediction": prediction["label"],
                    "confidence": prediction["confidence"],
                    "created_at": result_payload["created_at"],
                }
            )
            logger.info(
                "Prediction complete file=%s class=%s confidence=%.2f",
                incoming_file.filename,
                prediction["label"],
                prediction["confidence"],
            )
        except OCRServiceError as exc:
            logger.exception("OCR failure for %s", incoming_file.filename)
            results.append(
                {"filename": incoming_file.filename, "status": "error", "error": f"OCR failure: {exc}"}
            )
        except Exception as exc:
            logger.exception("Unexpected processing failure for %s", incoming_file.filename)
            results.append(
                {
                    "filename": incoming_file.filename,
                    "status": "error",
                    "error": f"Processing failed: {exc}",
                }
            )

    if not results:
        return render_template("index.html", history=HISTORY[:10], error="No valid files found.")
    return render_template("result.html", results=results, history=HISTORY[:10])


@main_bp.route("/history", methods=["GET"])
def history():
    return jsonify(HISTORY)


@main_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "AI Document Intelligence API online"})


@main_bp.route("/home", methods=["GET"])
def home_redirect():
    return redirect(url_for("main.index"))
