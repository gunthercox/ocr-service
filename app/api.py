
"""
OCR Service API
===============

This module provides a Flask API for performing OCR (Optical Character Recognition)
on uploaded images using Tesseract via pytesseract.
"""

from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    """
    Perform OCR on an uploaded image.

    Expects a POST request with a file field named 'image'.
    Returns the extracted text in JSON format.

    Returns
    -------
    flask.Response
        JSON response containing the extracted text or an error message.
    """
    if 'image' not in request.files:
        return jsonify(
            error={
                'image': 'This field is required.'
            }
        ), 400

    image = Image.open(request.files['image'])

    image_text = pytesseract.image_to_string(
        image,
        lang='eng'
    )

    return jsonify({
        'text': image_text
    })
