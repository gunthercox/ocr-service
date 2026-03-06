"""
Add SEO-optimized meta descriptions to documentation pages.
"""

# Page-specific meta descriptions optimized for search queries
META_DESCRIPTIONS = {
    'index': (
        'OCR REST API service supporting Tesseract and PaddleOCR engines. '
        'Extract text from images with Docker deployment. Fast, reliable document '
        'OCR and multi-directional text recognition.'
    ),
    'api': (
        'OCR API documentation: REST endpoints for text extraction from images. '
        'Supports Tesseract and PaddleOCR engines with 140+ languages. '
        'Multipart form-data uploads with JSON responses.'
    ),
    'deployment': (
        'Deploy OCR service with Docker and docker-compose. Choose from combined, '
        'Tesseract-only, or PaddleOCR-only image variants. Complete deployment guide '
        'with security considerations.'
    ),
    'architecture': (
        'OCR service architecture overview: API layer, engine routing, and processing '
        'pipeline. Learn how PaddleOCR and Tesseract engines are integrated and '
        'handle text recognition requests.'
    ),
    'modules': (
        'Python API reference for OCR service modules. Detailed documentation of '
        'functions, classes, and methods for Tesseract and PaddleOCR integration.'
    ),
    'development': (
        'OCR service development guide: running tests, linting, building documentation. '
        'Setup instructions for contributing to the Tesseract and PaddleOCR REST API service.'
    ),
}


def add_meta_description(app, pagename, templatename, context, doctree):
    """
    Add meta description tag to page context.
    """
    description = META_DESCRIPTIONS.get(pagename, META_DESCRIPTIONS['index'])
    context['metatags'] = context.get('metatags', '') + (
        f'<meta name="description" content="{description}" />\n'
        f'<meta property="og:description" content="{description}" />\n'
    )


def setup(app):
    app.connect('html-page-context', add_meta_description)
