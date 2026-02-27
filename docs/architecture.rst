Architecture
============

Overview
--------

The OCR service provides a REST API for extracting text from images using Tesseract OCR. It is designed to be simple, modular, and easy to integrate into other systems.

Component Diagram
-----------------

The service consists of the following main components:

- **API Layer**: Handles HTTP requests and responses using Flask.
- **OCR Engine**: Uses pytesseract and PIL to process images and extract text.
- **Error Handling**: Manages validation and error responses.

API Layer
---------

- Built with Flask.
- Exposes a single POST endpoint (`/`) for image uploads.
- Accepts multipart/form-data requests with an `image` file field.
- Returns JSON responses with extracted text or error messages.

OCR Processing
--------------

- Images are received via the API and stored in memory while being processed.
- `Tesseract <https://github.com/tesseract-ocr/tesseract>`__ (via `pytesseract <https://github.com/madmaze/pytesseract>`__) performs OCR on the image, extracting English text by default.
- The result is returned as a JSON object.

Error Handling
--------------

- If the `image` field is missing, a 400 error is returned with a descriptive message.
- Other errors (e.g., invalid image format) are handled gracefully and reported in the response.

Dependencies
------------

- **Flask**: Web framework for the API.
- **pytesseract**: Python wrapper for Tesseract OCR.

Data Flow
---------

1. Client sends a POST request with an image file to the API.
2. API validates the request and extracts the image.
3. Image is processed and passed to Tesseract for OCR.
4. Extracted text is returned in a JSON response.
5. Errors are reported in JSON format with appropriate status codes.
