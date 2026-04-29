# AI Document Intelligence Platform (OCR + ML)

NovaDocs AI is a hackathon-ready, production-style document intelligence system built with Flask, OpenCV, Tesseract OCR, and scikit-learn.

It supports:
- Multi-file upload and analysis
- OCR with advanced preprocessing pipeline
- ML-based classification (`invoice`, `resume`, `report`)
- Confidence scoring and progress visualization
- Structured key information extraction
- Processed image preview
- JSON export for each processed document
- Classification history dashboard
- Full logging and robust error handling

---

## Architecture

### High-level Flow
1. User uploads one or many document images from the modern web dashboard.
2. Each image is preprocessed with OpenCV:
   - grayscale
   - denoising
   - adaptive thresholding
   - edge detection
3. OCR is performed via `pytesseract`.
4. OCR text is normalized:
   - noisy token cleanup
   - stopword removal
   - stemming
5. TF-IDF + Logistic Regression predicts document class and confidence.
6. Domain extraction engine returns structured info:
   - invoice -> amount, date, invoice number
   - resume -> skills, education keywords
   - report -> headings/sections
7. UI renders card-based results including:
   - predicted class
   - confidence bar
   - extracted text
   - original + processed image
   - download JSON

### Text Architecture Diagram
```text
Browser UI
   |
   v
Flask Routes (routes/main_routes.py)
   |
   +--> OCR Service (services/ocr_service.py)
   |       |
   |       +--> Image Processing (utils/image_processing.py)
   |       +--> pytesseract OCR
   |
   +--> Text Processing (utils/text_processing.py)
   |
   +--> ML Service (services/ml_service.py)
   |       |
   |       +--> model.pkl + vectorizer.pkl
   |
   +--> Extraction Service (services/extraction_service.py)
   |
   v
Templates + Static Frontend (templates/, static/)
```

---

## Project Structure

```text
AI-Document-Intelligence/
├── app.py
├── app.log
├── requirements.txt
├── routes/
│   ├── __init__.py
│   └── main_routes.py
├── services/
│   ├── __init__.py
│   ├── ocr_service.py
│   ├── ml_service.py
│   └── extraction_service.py
├── model/
│   ├── train.py
│   ├── model.pkl
│   └── vectorizer.pkl
├── utils/
│   ├── __init__.py
│   ├── image_processing.py
│   └── text_processing.py
├── templates/
│   ├── index.html
│   ├── result.html
│   └── dashboard.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    └── uploads/
        ├── original/
        ├── processed/
        └── results/
```

---

## Setup and Run

### 1) Create and activate virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Install Tesseract OCR engine
`pytesseract` requires native Tesseract.

- Windows: [UB Mannheim Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt install tesseract-ocr`
- macOS: `brew install tesseract`

If not in PATH, set:
```powershell
$env:TESSERACT_CMD="C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### 4) Train model (optional - auto-trains if missing)
```bash
python model/train.py
```

### 5) Run app
```bash
python app.py
```

Open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Training Dataset Upgrade

The model uses a realistic in-code dataset with **18 samples per class** (total 54):
- Invoice examples with invoice ids, dates, totals, taxes, payment details
- Resume examples with skills, degree keywords, achievements, certifications
- Report examples with section headers, findings, recommendations, conclusions

Model stack:
- `TfidfVectorizer` with uni/bi-grams
- `LogisticRegression` classifier

---

## Logging and Error Handling

### Logs (`app.log`)
Tracks:
- uploads
- predictions with confidence
- OCR failures
- unexpected processing errors

### Error Scenarios Handled
- invalid file type
- empty file selection
- OCR failure / Tesseract unavailable
- noisy OCR resulting in empty normalized text
- generic runtime failures with user-safe messages

---

## Screenshots

Add screenshots after running the app:
- `screenshots/home.png` - upload dashboard with drag and drop
- `screenshots/results.png` - result cards with confidence bar and extracted info
- `screenshots/dashboard.png` - classification history dashboard

---

## Hackathon Demo Tips

- Use mixed sample documents in one upload for a strong multi-file demo.
- Show original vs processed image to explain OCR quality improvements.
- Download JSON outputs to demonstrate integration readiness.
