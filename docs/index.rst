ocr-service documentation
=========================

**OCR Service** is a production-ready REST API for optical character recognition (OCR) that supports both **Tesseract** and **PaddleOCR** engines. Extract text from images with high accuracy using a simple HTTP API. Deploy easily with Docker for document processing, invoice scanning, multi-language text recognition, and automated data extraction workflows.

Key Features
------------

* **Dual OCR Engines**: Choose between Tesseract (fast document OCR) and PaddleOCR (multi-directional text)
* **REST API**: Simple multipart/form-data POST requests with JSON responses
* **140+ Languages**: Comprehensive language support via Tesseract language packs
* **Docker Ready**: Pre-built images on Docker Hub with variant options
* **Production Grade**: Health checks, error handling, and security best practices included

Quick Start
-----------

Get started with the OCR API in seconds using Docker:

.. code-block:: bash

   # Pull and run the default image (both engines)
   docker run -p 5000:5000 gunthercox/ocr-service:latest

   # Extract text from an image
   curl -X POST -F "image=@document.png" http://localhost:5000/

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   deployment
   architecture
   modules
   development

   GitHub ↗ <https://github.com/gunthercox/ocr-service>
   Docker Hub ↗ <https://hub.docker.com/r/gunthercox/ocr-service>

Frequently Asked Questions
--------------------------

**Which OCR engine should I use?**
   Use **Tesseract** for well-aligned document OCR (invoices, forms, scanned pages). Use **PaddleOCR** for rotated text, multi-directional layouts, or challenging image orientations.

**How many languages are supported?**
   Over 140 languages are supported through Tesseract. PaddleOCR supports 80+ languages including Chinese, Japanese, Korean, and many Latin-script languages.

**Can I use this for commercial projects?**
   Yes, the service is open source. Check the LICENSE for details on both the service and underlying OCR engines.

**What image formats are supported?**
   PNG, JPEG, WebP, TIFF, BMP, and most common image formats are supported by both OCR engines.
