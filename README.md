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
