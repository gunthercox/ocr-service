API
===

This document provides a reference for the REST API of the OCR service.
It describes the available endpoints, their expected inputs and outputs,
and any relevant details for using the API effectively.

Endpoint: /
-----------

**Method:** POST

**Description:**
Performs OCR on an uploaded image using the specified OCR engine.
Expects a file field named `image` in the request, and accepts optional
parameters to control the OCR engine and language.

**Request:**

- Content-Type: multipart/form-data
- Maximum file size: 10MB
- Form fields:
  
  - ``image`` (file, required): The image file to process
  - ``engine`` (string, optional): OCR engine to use - 'tesseract' or 'paddleocr' (default: 'paddleocr')
  - ``lang`` (string, optional): Language code (format depends on engine, see below)

**Supported Engines:**

- **tesseract**: Fast and efficient for standard document OCR with well-aligned text
- **paddleocr**: Better for multi-directional and rotated text (default)

**Example (cURL):**

.. code-block:: bash

   # Using default engine (PaddleOCR)
   curl -X POST \
        -F "image=@example.png" \
        http://localhost:5000/

   # Using Tesseract engine with Japanese language
   curl -X POST \
        -F "image=@example.png" \
        -F "engine=tesseract" \
        -F "lang=jpn" \
        http://localhost:5000/

   # Using PaddleOCR engine with Chinese language
   curl -X POST \
        -F "image=@example.png" \
        -F "engine=paddleocr" \
        -F "lang=ch" \
        http://localhost:5000/

**Response:**

- Content-Type: application/json

**Success Example (PaddleOCR):**

.. code-block:: json

   {
     "text": "Concatenated text from all detected regions",
     "regions": [
       {
         "bbox": [[10, 20], [100, 20], [100, 40], [10, 40]],
         "text": "Detected text",
         "confidence": 0.95
       },
       {
         "bbox": [[10, 50], [120, 50], [120, 70], [10, 70]],
         "text": "Another text region",
         "confidence": 0.92
       }
     ]
   }

**Success Example (Tesseract):**

.. code-block:: json

   {
     "text": "Extracted OCR text from the image.",
     "regions": [
       {
         "bbox": [[15, 25], [95, 25], [95, 42], [15, 42]],
         "text": "Extracted",
         "confidence": 0.96
       },
       {
         "bbox": [[100, 25], [140, 25], [140, 42], [100, 42]],
         "text": "OCR",
         "confidence": 0.94
       }
     ]
   }

**Response Fields:**

- ``text`` (string): All detected text (concatenated with spaces for PaddleOCR, full text for Tesseract)
- ``regions`` (array): List of detected text regions (both engines provide this data)
  
  Each region contains:
  
  - ``bbox`` (array): Bounding box as 4 corner points [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
  - ``text`` (string): The text content from this region
  - ``confidence`` (float): Confidence score from 0.0 to 1.0

**Error Example (missing image field):**

.. code-block:: json

   {
     "error": {
       "image": "This field is required."
     }
   }

**Error Example (invalid engine):**

.. code-block:: json

   {
     "error": {
       "engine": "Unsupported engine: invalid. Must be one of: tesseract, paddleocr"
     }
   }

**Error Example (file too large):**

.. code-block:: json

   {
     "error": {
       "image": "File size exceeds 10MB limit."
     }
   }

**Error Example (invalid content type):**

.. code-block:: json

   {
     "error": {
       "content_type": "Request must be multipart/form-data."
     }
   }

**Status Codes:**

- 200: Success, returns extracted text and regions.
- 400: Bad request, missing or invalid parameters.
- 413: Payload too large, file exceeds 10MB limit.

Endpoint: /health
-----------------

**Method:** GET

**Description:**
Health check endpoint to verify the service is running and responsive.

**Request:**

No parameters required.

**Example (cURL):**

.. code-block:: bash

   curl http://localhost:5000/health

**Response:**

- Status Code: 200
- Empty response body

**Status Codes:**

- 200: Service is healthy and operational.

Supported Languages
-------------------

The language codes and available languages depend on which OCR engine you use:

**Tesseract Languages**

All Tesseract language and script packs installed in the container are supported.
For the full list, see the Dockerfile in this repository.

Common language codes:

============  ======================
Code          Language
============  ======================
eng           English
fra           French
jpn           Japanese
deu           German
spa           Spanish
chi_sim       Chinese Simplified
chi_tra       Chinese Traditional
rus           Russian
ara           Arabic
hin           Hindi
por           Portuguese
eng+fra       English + French (multi-language)
============  ======================

Multi-language OCR is supported using the ``+`` operator (e.g., ``eng+fra`` for English and French).

**PaddleOCR Languages**

PaddleOCR supports 80+ languages. Common language codes:

============  ======================
Code          Language
============  ======================
en            English
ch            Chinese Simplified
japan         Japanese
korean        Korean
fr            French
german        German
es            Spanish
pt            Portuguese
ru            Russian
ar            Arabic
hi            Hindi
============  ======================

For a complete list of supported PaddleOCR languages, see the
`PaddleOCR documentation <https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_en/multi_languages_en.md>`_.

**Important:** Language codes differ between engines. Ensure you use the correct
format for your selected engine. For example, Japanese is ``jpn`` in Tesseract but
``japan`` in PaddleOCR.

Supported Image Formats
------------------------

All image formats supported by the Python Pillow library are accepted, including:

- PNG
- JPEG/JPG
- BMP
- TIFF
- GIF
- WebP

Engine Comparison
-----------------

**When to use Tesseract:**

- Standard document OCR with well-aligned text
- Simple, clean layouts
- When speed is important
- When you need multi-language detection in a single pass (e.g., ``eng+fra``)

**When to use PaddleOCR:**

- Multi-directional text (text at various angles in the same image)
- Rotated or angled text
- Text in natural scenes and photographs
- Complex document layouts
- When you need bounding box coordinates and confidence scores

**Performance Notes:**

PaddleOCR is more computationally intensive than Tesseract and may take longer
to process images, especially on the first request (model initialization).
However, it provides significantly better accuracy for complex or rotated text.
