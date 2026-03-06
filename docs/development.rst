Development
===========

Development guide for contributing to the OCR service. Learn how to set up your local development environment, run tests, perform linting checks, and build the documentation for the Tesseract and PaddleOCR REST API.

**GitHub Repository**: https://github.com/gunthercox/ocr-service

Clone the repository and follow the instructions below to run the OCR service locally for development and testing.

Running the container
---------------------

This application is fully Dockerized and can be started with docker compose.

.. code:: bash

   docker compose up -d

Running Tests
-------------

.. code:: bash

   docker compose exec app python -m unittest discover -s tests/

Running Linting Checks
----------------------

.. code:: bash

   docker compose exec app python -m flake8 ./

Build Documentation
-------------------

.. code:: bash

   docker compose exec app python -m sphinx -b html docs/ html
