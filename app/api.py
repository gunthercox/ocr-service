
"""
OCR Service API
===============

This module provides a Flask API for performing OCR (Optical Character
Recognition) on uploaded images.
"""

from flask import Flask, request, jsonify
from PIL import Image
import logging
import os

# Configuration from environment variables
MAX_FILE_SIZE_BYTES = (
    int(os.environ.get('MAX_FILE_SIZE_MB', '10')) * 1024 * 1024
)

# Detect which OCR engines are actually available by attempting imports
# and verifying runtime availability
AVAILABLE_ENGINES = []

# Try importing and testing Tesseract
try:
    import pytesseract
    from pytesseract import Output
    AVAILABLE_ENGINES.append('tesseract')
except ImportError:
    pass

# Try importing PaddleOCR
try:
    from paddleocr import PaddleOCR
    AVAILABLE_ENGINES.append('paddleocr')
except ImportError:
    pass

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Lazy initialization for PaddleOCR to avoid race conditions with
# multiple workers
_paddle_ocr_instance = None


def get_paddle_ocr():
    """
    Get or initialize the global PaddleOCR instance.
    """
    global _paddle_ocr_instance
    if _paddle_ocr_instance is None:
        _paddle_ocr_instance = PaddleOCR(
            use_angle_cls=True, lang='en', show_log=False
        )
    return _paddle_ocr_instance


def _process_with_tesseract(image, lang='eng'):
    """
    Process an image using Tesseract OCR with bounding box detection.

    Parameters
    ----------
    image : PIL.Image
        The image to process.
    lang : str, optional
        Language code for Tesseract (default: 'eng').

    Returns
    -------
    dict
        Dictionary containing 'text' (concatenated text) and 'regions' (list of
        detected text regions with bounding boxes and confidence scores).
    """
    # Get detailed data including bounding boxes and confidence
    data = pytesseract.image_to_data(
        image, lang=lang, output_type=Output.DICT
    )

    # Also get the full text
    full_text = pytesseract.image_to_string(image, lang=lang)

    regions = []
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        # Only include entries with actual text and confidence > 0
        text = data['text'][i].strip()
        conf = int(data['conf'][i])

        if text and conf > 0:
            # Get bounding box coordinates
            x, y, w, h = (
                data['left'][i], data['top'][i],
                data['width'][i], data['height'][i]
            )

            # Convert to corner points format like PaddleOCR:
            # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            bbox = [
                [x, y],           # top-left
                [x + w, y],       # top-right
                [x + w, y + h],   # bottom-right
                [x, y + h]        # bottom-left
            ]

            regions.append({
                'bbox': bbox,
                'text': text,
                # Convert to 0.0-1.0 range like PaddleOCR
                'confidence': conf / 100.0
            })

    return {
        'text': full_text,
        'regions': regions
    }


def _process_with_paddleocr(image, ocr_instance=None):
    """
    Process an image using PaddleOCR for multi-directional text detection.

    Parameters
    ----------
    image : PIL.Image
        The image to process.
    ocr_instance : PaddleOCR, optional
        PaddleOCR instance to use. If None, uses the default instance.

    Returns
    -------
    dict
        Dictionary containing 'text' (concatenated text) and 'regions' (list of
        detected text regions with bounding boxes and confidence scores).
    """
    import numpy as np

    if ocr_instance is None:
        ocr_instance = get_paddle_ocr()

    # Convert PIL Image to numpy array for PaddleOCR
    img_array = np.array(image)

    # Run PaddleOCR
    result = ocr_instance.ocr(img_array, cls=True)

    # Parse results
    regions = []
    all_text = []

    if result and result[0]:
        for line in result[0]:
            bbox = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            text_info = line[1]  # (text, confidence)
            text = text_info[0]
            confidence = float(text_info[1])

            regions.append({
                'bbox': bbox,
                'text': text,
                'confidence': confidence
            })
            all_text.append(text)

    return {
        'text': ' '.join(all_text),
        'regions': regions
    }


@app.route('/', methods=['POST'])
def index():
    """
    Perform OCR on an uploaded image.

    Expects a POST request with:
      - a file field named 'image' (the image to process)
      - an optional form field 'engine' to specify the OCR engine
        ('tesseract' or 'paddleocr'). If not provided, defaults to 'paddleocr'.
      - an optional form field 'lang' to specify OCR language(s).
        The language code format depends on the engine:
        * Tesseract: 'eng', 'jpn', 'fra', 'eng+fra', 'chi_sim', etc.
        * PaddleOCR: 'en', 'japan', 'fr', 'ch', 'korean', etc.

    File size limit: Configurable via MAX_FILE_SIZE_MB environment variable
    (default: 10MB).

    Example (using curl):
        curl -X POST -F "image=@/img.png" http://localhost:5000/
        curl -X POST -F "image=@/img.png" -F "engine=tesseract" \
            -F "lang=jpn" http://localhost:5000/
        curl -X POST -F "image=@/img.png" -F "engine=paddleocr" \
            -F "lang=ch" http://localhost:5000/

    Returns the extracted text and detected regions in JSON format.

    Returns
    -------
    flask.Response
        JSON response containing:
        - text: Concatenated extracted text from all regions
        - regions: List of detected text regions (both engines provide bounding
          boxes)
          Each region contains:
          - bbox: Bounding box coordinates [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
          - text: Extracted text for this region
          - confidence: Confidence score (0.0 to 1.0)

    Supported Engines
    ----------------
    - tesseract: Fast and efficient for standard document OCR
    - paddleocr: Better for multi-directional and rotated text (default)

    Supported Languages
    ------------------
    **Tesseract**: All Tesseract language and script packs installed in the
    container are supported. Common examples include:
        - English (eng)
        - French (fra)
        - Japanese (jpn)
        - German (deu)
        - Spanish (spa)
        - Chinese (chi_sim, chi_tra)
        - Russian (rus)
        - Arabic (ara)
        - (See Dockerfile for included Tesseract languages)

    **PaddleOCR**: Supports 80+ languages including:
        - English (en)
        - Chinese Simplified (ch)
        - Japanese (japan)
        - Korean (korean)
        - French (fr)
        - German (german)
        - Spanish (es)
        - Portuguese (pt)
        - Russian (ru)
        - Arabic (ar)

    Supported File Formats
    ---------------------
    All image formats supported by the Python Pillow library, including:
        - PNG
        - JPEG/JPG
        - BMP
        - TIFF
    """
    # Validate Content-Type
    if (not request.content_type or
            'multipart/form-data' not in request.content_type):
        return jsonify(
            error={
                'content_type': 'Request must be multipart/form-data.'
            }
        ), 400

    # Validate file size
    if request.content_length and request.content_length > MAX_FILE_SIZE_BYTES:
        limit_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
        return jsonify(
            error={
                'image': f'File size exceeds {limit_mb}MB limit.'
            }
        ), 413

    if 'image' not in request.files:
        return jsonify(
            error={
                'image': 'This field is required.'
            }
        ), 400

    # Get engine parameter, default to first available engine if not provided
    # For single-engine Docker images, this will be the only installed engine
    if not AVAILABLE_ENGINES:
        return jsonify(
            error={
                'engine': (
                    'No OCR engines are available. Please use a Docker '
                    'image with at least one engine installed.'
                )
            }
        ), 500

    default_engine = AVAILABLE_ENGINES[0]
    engine = request.form.get('engine', default_engine).strip().lower()
    if not engine:
        engine = default_engine

    # Validate engine is supported and available in this image variant
    if engine not in AVAILABLE_ENGINES:
        return jsonify(
            error={
                'engine': (
                    f"Engine '{engine}' is not available in this image "
                    f"variant. Available engines: "
                    f"{', '.join(AVAILABLE_ENGINES)}. Please use an image "
                    f"with the '{engine}' engine installed."
                )
            }
        ), 400

    # Get language parameter with engine-specific defaults
    if engine == 'tesseract':
        lang = request.form.get('lang', 'eng').strip()
        if not lang:
            lang = 'eng'
    else:  # paddleocr
        lang = request.form.get('lang', 'en').strip()
        if not lang:
            lang = 'en'

    try:
        image = Image.open(request.files['image'])
    except Exception as e:
        app.logger.exception(
            "Failed to open image file",
            exc_info=e
        )
        return jsonify(error={
            'image': (
                'Failed to process image. Please ensure the image is '
                'valid.'
            )
        }), 400

    # Route to appropriate engine
    if engine == 'tesseract':
        try:
            # Process with Tesseract and get regions with bounding boxes
            result = _process_with_tesseract(image, lang)
            return jsonify(result)
        except pytesseract.TesseractError as e:
            app.logger.exception(
                "Tesseract OCR failed for requested language(s): %s",
                lang,
                exc_info=e
            )
            return jsonify(error={
                'lang': f"Failed to use language(s): {lang}"
            }), 400

    else:  # paddleocr
        # Reinitialize PaddleOCR if language changes (for optimal performance)
        # Note: In production, consider caching OCR instances per language
        try:
            if lang != 'en':
                ocr_instance = PaddleOCR(
                    use_angle_cls=True, lang=lang, show_log=False
                )
            else:
                ocr_instance = get_paddle_ocr()
        except Exception as e:
            app.logger.exception(
                "Failed to initialize PaddleOCR for language: %s",
                lang,
                exc_info=e
            )
            return jsonify(error={
                'lang': f"Failed to use language: {lang}"
            }), 400

        try:
            # Process with PaddleOCR
            result = _process_with_paddleocr(image, ocr_instance)
            return jsonify(result)

        except Exception as e:
            app.logger.exception(
                "PaddleOCR failed for language: %s",
                lang,
                exc_info=e
            )
            return jsonify(error={
                'processing': (
                    'Failed to process image. Please ensure the image is '
                    'valid.'
                )
            }), 400


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.

    Returns a 200 status code to indicate the service is running.

    Example (using curl):
        curl http://localhost:5000/health

    Returns
    -------
    flask.Response
        Empty response with 200 status code.
    """
    return '', 200
