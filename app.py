import logging
from pathlib import Path

from flask import Flask

from routes.main_routes import main_bp
from services.ml_service import bootstrap_model


BASE_DIR = Path(__file__).resolve().parent


def create_app() -> Flask:
    log_path = BASE_DIR / "app.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "hackathon-document-intelligence"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = str(BASE_DIR / "static" / "uploads" / "original")
    app.config["PROCESSED_FOLDER"] = str(BASE_DIR / "static" / "uploads" / "processed")
    app.config["RESULTS_FOLDER"] = str(BASE_DIR / "static" / "uploads" / "results")
    app.register_blueprint(main_bp)
    return app


app = create_app()
bootstrap_model()

if __name__ == "__main__":
    app.run(debug=True)
