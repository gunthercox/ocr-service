
"""
OCR Service API
===============

This module provides a Flask API for performing OCR (Optical Character
Recognition) on uploaded images using Tesseract via pytesseract.
"""

from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['POST'])
def index():
    """
    Perform OCR on an uploaded image.

    Expects a POST request with:
      - a file field named 'image' (the image to process)
      - an optional form field 'lang' to specify OCR language(s)
        (e.g., 'eng', 'jpn', 'fra', or 'eng+fra').
        If not provided, defaults to 'eng'.

    Example (using curl):
        curl -X POST -F "image=@/img.png" -F "lang=jpn" http://localhost:5000/

    Returns the extracted text in JSON format.

    Returns
    -------
    flask.Response
        JSON response containing the extracted text or an error message.

    Supported Languages
    ------------------
    All Tesseract language and script packs installed in the container are
    supported. For the full list, see the Dockerfile in this repository.
    Common examples include:
        - English (eng)
        - French (fra)
        - Japanese (jpn)
        - German (deu)
        - Spanish (spa)
        - Chinese (chi_sim, chi_tra)
        - Russian (rus)
        - Arabic (ara)
        - and many more (see Dockerfile for included language packs).

    Supported File Formats
    ---------------------
    All image formats supported by the Python Pillow library, including:
        - PNG
        - JPEG/JPG
        - BMP
        - TIFF
    """
    if 'image' not in request.files:
        return jsonify(
            error={
                'image': 'This field is required.'
            }
        ), 400

    # Get language parameter, default to 'eng' if not provided
    lang = request.form.get('lang', 'eng').strip()
    if not lang:
        lang = 'eng'

    image = Image.open(request.files['image'])

    try:
        image_text = pytesseract.image_to_string(
            image,
            lang=lang
        )
    except pytesseract.TesseractError as e:
        app.logger.exception(
            "Tesseract OCR failed for requested language(s): %s",
            lang,
            exc_info=e
        )
        return jsonify(error={
            'lang': f"Failed to use language(s): {lang}"
        }), 400

    return jsonify({
        'text': image_text
    })
