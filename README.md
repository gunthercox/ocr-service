# OCR Service

This is a stand alone character recognition microservice
that can be accessed via a REST API.

The service's expects json in the following format:

```json
{
    'image': '<image byte content>'
}
```

Data will be returned in the following format:

```json
{
    "text": [
        "Line of text one",
        "Line of text two"
    ]
}
```

## Running the container

This application is fully Dockerized and can be started with docker compose.

```bash
docker compose up -d
```
