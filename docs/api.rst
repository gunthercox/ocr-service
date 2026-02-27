API
===

This document provides a reference for the REST API of the OCR service.
It describes the available endpoints, their expected inputs and outputs,
and any relevant details for using the API effectively.

Endpoint: /
-----------

**Method:** POST

**Description:**
Performs OCR on an uploaded image. Expects a file field named `image` in the request.

**Request:**

- Content-Type: multipart/form-data
- Form field: `image` (file)

**Example (cURL):**

.. code-block:: bash

   curl -X POST \
        -F "image=@example.png" \
        http://localhost:5000/

**Response:**

- Content-Type: application/json

**Success Example:**

.. code-block:: json

   {
     "text": "Extracted OCR text from the image."
   }

**Error Example (missing image field):**

.. code-block:: json

   {
     "error": {
       "image": "This field is required."
     }
   }

**Status Codes:**

- 200: Success, returns extracted text.
- 400: Bad request, missing or invalid image field.
