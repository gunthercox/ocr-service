# OCR Service

This is a stand alone character recognition microservice
that can be accessed via a REST API.

The service's expects json in the following format:

```
{
    'image': '63469ef70377ee9a23b7b8ec5'
}
```

where the image is a base 64 encoded image.

Data will be returned in the following format:

```
{
    "text": [
        "Line of text one",
        "Line of text two"
    ]
}
```