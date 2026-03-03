# OCR Service

This is a stand alone character recognition microservice
that can be accessed via a REST API.

The service supports two OCR engines:
- **Tesseract**: Fast and efficient for standard document OCR
- **PaddleOCR**: Better for multi-directional and rotated text (default)

## Documentation

https://gunthercox.com/ocr-service/

## Docker Hub Image

https://hub.docker.com/r/gunthercox/ocr-service

### Available Image Variants

The service provides three Docker image variants to suit different deployment needs:

1. **Combined (default)** - Both engines available
   ```bash
   docker pull gunthercox/ocr-service:latest
   docker pull gunthercox/ocr-service:1.0.0
   ```
   - Python 3.12
   - Includes both Tesseract and PaddleOCR
   - Largest image size (includes 140+ Tesseract language packs)
   - Use when you need flexibility to choose engines per request

2. **Tesseract only** - Smaller image for document OCR
   ```bash
   docker pull gunthercox/ocr-service:latest-tesseract
   docker pull gunthercox/ocr-service:1.0.0-tesseract
   ```
   - Python 3.12
   - Includes only Tesseract with all language packs
   - Use for standard document OCR workloads

3. **PaddleOCR only** - Smallest image, newest Python
   ```bash
   docker pull gunthercox/ocr-service:latest-paddleocr
   docker pull gunthercox/ocr-service:1.0.0-paddleocr
   ```
   - Python 3.13
   - Includes only PaddleOCR (no Tesseract language packs)
   - Smallest image size
   - Use for rotated/multi-directional text or when image size matters

**Note**: Engine-specific images will return an error if you request an unavailable engine. For example, the Tesseract-only image will reject requests when `engine=paddleocr` is specified in the request body.

## API Usage

The service expects a multipart/form-data request with the following fields:

- `image` (required): The image file to process
- `engine` (optional): 'tesseract' or 'paddleocr' (default: 'paddleocr')
- `lang` (optional): Language code (format depends on engine)

### Example Request

```bash
# Using default engine (PaddleOCR)
curl -X POST -F "image=@example.png" http://localhost:5000/

# Using Tesseract engine
curl -X POST -F "image=@example.png" -F "engine=tesseract" -F "lang=eng" http://localhost:5000/

# Using PaddleOCR with Chinese
curl -X POST -F "image=@example.png" -F "engine=paddleocr" -F "lang=ch" http://localhost:5000/
```

### Response Format

Data will be returned in the following format:

```json
{
    "text": "Extracted text from the image",
    "regions": [
        {
            "bbox": [[10, 20], [100, 20], [100, 40], [10, 40]],
            "text": "Detected text",
            "confidence": 0.95
        }
    ]
}
```
