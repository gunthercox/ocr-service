Deployment
==========

The OCR service can be deployed using Docker for easy setup and portability.

Deployment using docker-compose
-------------------------------

For production environments, it is recommended to use the official Docker image from Docker Hub. Below is an example `docker-compose.yml` for deploying the OCR service in production:

.. code-block:: yaml
  :caption: docker-compose.yml

   services:
     ocr-service:
       image: gunthercox/ocr-service:latest
       ports:
         - "5000:5000"
       restart: unless-stopped

You can also pin to a specific version for more predictable deployments:

.. code-block:: yaml
  :caption: docker-compose.yml

   services:
     ocr-service:
       image: gunthercox/ocr-service:1.1.2
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
