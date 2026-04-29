from __future__ import annotations

import cv2
import numpy as np


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    thresholded = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11
    )
    edges = cv2.Canny(thresholded, 75, 200)
    merged = cv2.bitwise_or(thresholded, edges)
    kernel = np.ones((1, 1), np.uint8)
    final = cv2.morphologyEx(merged, cv2.MORPH_CLOSE, kernel)
    return final
