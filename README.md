# OCR Service

This is a stand alone character recognition microservice
that can be accessed via a REST API.

The service's expects json in the following format:

```
{
    'image': '<image byte content>'
}
```

Data will be returned in the following format:

```
{
    "text": [
        "Line of text one",
        "Line of text two"
    ]
}
```

## Running the container

This application is fully Dockerized and can be started with docker-compose.

```
docker-compose up
```
