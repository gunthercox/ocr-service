Deployment
==========

The OCR service can be deployed using Docker for easy setup and portability.
Tagged builds are available on Docker Hub:
https://hub.docker.com/r/gunthercox/ocr-service

Image Variants
--------------

The service provides three Docker image variants optimized for different use cases:

**Combined (default)** - Both engines available
  Use when you need flexibility to switch between OCR engines per request.

  - Tags: ``latest``, ``1.0.0``, ``1.0``
  - Python version: 3.12
  - Includes: Tesseract + PaddleOCR
  - Size: Largest (includes 140+ Tesseract language packs)
  - Available engines: Both ``tesseract`` and ``paddleocr``

**Tesseract only** - Document OCR
  Optimized for standard document OCR workloads.

  - Tags: ``latest-tesseract``, ``1.0.0-tesseract``, ``1.0-tesseract``
  - Python version: 3.12
  - Includes: Tesseract with all language packs
  - Size: Medium
  - Available engines: Only ``tesseract``

**PaddleOCR only** - Modern OCR with latest Python
  Best for rotated/multi-directional text or size-constrained environments.

  - Tags: ``latest-paddleocr``, ``1.0.0-paddleocr``, ``1.0-paddleocr``
  - Python version: 3.13
  - Includes: PaddleOCR only
  - Size: Smallest
  - Available engines: Only ``paddleocr``

**Important**: Engine-specific images will return a 400 error if you request an unavailable engine. For example:

.. code-block:: bash

   # This will fail with Tesseract-only image
   curl -X POST -F "image=@photo.png" -F "engine=paddleocr" http://localhost:5000/

The error response will indicate which engines are available in the deployed image variant.

Deployment using docker-compose
-------------------------------

For production environments, it is recommended to use the official Docker image from Docker Hub. Below is an example `docker-compose.yml` for deploying the OCR service in production:

**Combined variant** (default, both engines):

.. code-block:: yaml
  :caption: docker-compose.yml

   services:
     ocr-service:
       image: gunthercox/ocr-service:latest
       ports:
         - "5000:5000"
       restart: unless-stopped

**Tesseract-only variant** (smaller, document OCR):

.. code-block:: yaml
  :caption: docker-compose.yml

   services:
     ocr-service:
       image: gunthercox/ocr-service:latest-tesseract
       ports:
         - "5000:5000"
       restart: unless-stopped

**PaddleOCR-only variant** (smallest, Python 3.13):

.. code-block:: yaml
  :caption: docker-compose.yml

   services:
     ocr-service:
       image: gunthercox/ocr-service:latest-paddleocr
       ports:
         - "5000:5000"
       restart: unless-stopped

You can also pin to a specific version for more predictable deployments:

.. code-block:: yaml
  :caption: docker-compose.yml

   services:
     ocr-service:
       image: gunthercox/ocr-service:1.1.2-paddleocr
       ports:
         - "5000:5000"
       restart: unless-stopped

To run the service using docker-compose, run the following command in the directory containing your `docker-compose.yml` file:

  .. code-block:: bash

     docker compose up -d

- The service will be available at `http://localhost:5000/` by default.

Security Considerations
-----------------------

- For production, consider using a reverse proxy (e.g., Nginx) in front of the service for SSL termination and additional security.
- Monitor and update the image regularly to receive security and feature updates.
- Validate and sanitize all uploaded files to prevent malicious input.
- Limit accepted file types to images only.
- Consider rate limiting and authentication for production deployments.

**Additional Notes:**

- Review the `Docker Hub page <https://hub.docker.com/r/gunthercox/ocr-service>`_ for available tags.
