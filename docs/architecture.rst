Architecture
============

Overview
--------

The OCR service provides a REST API for extracting text from images using two OCR engines: Tesseract and PaddleOCR. It is designed to be simple, modular, and easy to integrate into other systems. The service allows clients to choose between engines to optimize for either speed (Tesseract) or accuracy with complex/rotated text (PaddleOCR).

Component Diagram
-----------------

The service consists of the following main components:

- **API Layer**: Handles HTTP requests and responses using Flask.
- **OCR Engine Router**: Directs requests to the appropriate OCR engine based on the `engine` parameter.
- **Tesseract Engine**: Fast OCR for standard documents using pytesseract and PIL.
- **PaddleOCR Engine**: Advanced OCR for multi-directional and rotated text using PaddleOCR.
- **Validation Layer**: Manages request validation including file size, content type, and parameter validation.
- **Error Handling**: Manages validation and error responses.

API Layer
---------

- Built with Flask.
- Exposes a single POST endpoint (`/`) for image uploads.
- Accepts multipart/form-data requests with the following fields:

  - ``image`` (required): The image file to process
  - ``engine`` (optional): 'tesseract' or 'paddleocr' (default: 'paddleocr')
  - ``lang`` (optional): Language code (format depends on engine)

- Validates Content-Type and enforces 10MB file size limit.
- Returns JSON responses with extracted text and regions or error messages.

OCR Engine Routing
------------------

The service supports two OCR engines and can be deployed with different combinations:

Engine Availability
~~~~~~~~~~~~~~~~~~~

The available engines are determined by the Docker image variant deployed:

- **Combined image** (default): Both engines available
- **Tesseract-only image**: Only Tesseract available
- **PaddleOCR-only image**: Only PaddleOCR available

**Engine Validation**: When a request is received, the service validates that the requested engine is available in the current deployment. If an unavailable engine is requested, the service returns a 400 error with a message indicating which engines are available.

Example error response from a Tesseract-only image when PaddleOCR is requested:

.. code-block:: json

   {
     "error": {
       "engine": "Engine 'paddleocr' is not available in this image variant. Available engines: tesseract. Please use an image with the 'paddleocr' engine installed."
     }
   }

**Conditional Imports**: OCR engine libraries are installed and imported conditionally. This means:

- Tesseract-only images don't install PaddleOCR dependencies
- PaddleOCR-only images don't install pytesseract dependencies
- Combined images install dependencies for both

**Tesseract Engine (via pytesseract)**

- Fast and efficient for standard document OCR
- Suitable for well-aligned, horizontal text
- Returns text with bounding boxes and confidence scores
- Supports multi-language detection (e.g., 'eng+fra')
- Lightweight and quick processing

**PaddleOCR Engine**

- Advanced deep learning-based OCR engine
- Excels at multi-directional and rotated text
- Detects text at various angles in the same image
- Returns text with bounding boxes and confidence scores
- Better for natural scenes and complex layouts
- More computationally intensive and slower

**Default Engine:** PaddleOCR is the default engine due to its superior handling of multi-directional text and real-world images, despite being slower than Tesseract.

OCR Processing
--------------

**General Flow:**

1. Images are received via the API and validated
2. The `engine` parameter determines which OCR engine to use
3. Images are stored in memory during processing
4. The selected engine processes the image
5. Results are formatted as JSON and returned

**Tesseract Processing:**

- Images are passed to `Tesseract <https://github.com/tesseract-ocr/tesseract>`__ (via `pytesseract <https://github.com/madmaze/pytesseract>`__)
- Uses ``image_to_data()`` to extract text with bounding boxes and confidence scores
- Returns: ``{"text": "...", "regions": [{"bbox": [...], "text": "...", "confidence": 0.95}, ...]}``

**PaddleOCR Processing:**

- Images are converted to numpy arrays
- Passed to `PaddleOCR <https://github.com/PaddlePaddle/PaddleOCR>`__ with angle classification enabled
- Detects text regions with bounding boxes
- Extracts text from each region with confidence scores
- Returns: ``{"text": "...", "regions": [{"bbox": [...], "text": "...", "confidence": 0.95}, ...]}``

Error Handling
--------------

- If the `image` field is missing, a 400 error is returned with a descriptive message.
- If the requested engine is not available in the deployed image variant, a 400 error is returned indicating available engines.
- If the `engine` parameter is invalid, a 400 error is returned listing supported engines.
- If the file size exceeds 10MB, a 413 error is returned.
- If Content-Type is not multipart/form-data, a 400 error is returned.
- If the language is invalid for the selected engine, a 400 error is returned.
- Other errors (e.g., invalid image format) are handled gracefully and reported in the response.

Dependencies
------------

- **Flask**: Web framework for the API.
- **pytesseract**: Python wrapper for Tesseract OCR.
- **PaddleOCR**: Deep learning-based OCR system for multi-directional text.

Data Flow
---------

1. Client sends a POST request with an image file and optional engine/lang parameters to the API.
2. API validates the request (Content-Type, file size, required fields).
3. API validates the engine parameter and routes to the appropriate OCR engine.
4. Image is processed by the selected engine:

   - Tesseract: Fast text extraction
   - PaddleOCR: Text extraction with bounding boxes and confidence scores

5. Results are formatted as JSON with consistent structure (both engines return regions).
6. Extracted text and regions with bounding boxes are returned in a JSON response.
7. Errors are reported in JSON format with appropriate status codes.
