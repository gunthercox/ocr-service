#
# Multi-stage Dockerfile for OCR service with three build targets:
# - tesseract: Tesseract OCR only (Python 3.12)
# - paddleocr: PaddleOCR only (Python 3.13)
# - all: Both engines (Python 3.12) - default
#
# Build examples:
#   docker build --target tesseract -t ocr-service:tesseract .
#   docker build --target paddleocr -t ocr-service:paddleocr .
#   docker build --target all -t ocr-service:all .
#

# =============================================================================
# Target: tesseract (Tesseract OCR only, Python 3.12)
# =============================================================================
FROM python:3.12-slim AS tesseract

# Build argument to control whether to install dev dependencies
ARG INSTALL_DEV=false

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    FLASK_APP=app/api.py

# For a list of available Tesseract language packs, see:
# https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html

RUN apt-get update && apt-get install -y \
    # Tesseract OCR and language packs
    tesseract-ocr \
    tesseract-ocr-afr \
    tesseract-ocr-all \
    tesseract-ocr-amh \
    tesseract-ocr-ara \
    tesseract-ocr-asm \
    tesseract-ocr-aze \
    tesseract-ocr-aze-cyrl \
    tesseract-ocr-bel \
    tesseract-ocr-ben \
    tesseract-ocr-bod \
    tesseract-ocr-bos \
    tesseract-ocr-bre \
    tesseract-ocr-bul \
    tesseract-ocr-cat \
    tesseract-ocr-ceb \
    tesseract-ocr-ces \
    tesseract-ocr-chi-sim \
    tesseract-ocr-chi-sim-vert \
    tesseract-ocr-chi-tra \
    tesseract-ocr-chi-tra-vert \
    tesseract-ocr-chr \
    tesseract-ocr-cos \
    tesseract-ocr-cym \
    tesseract-ocr-dan \
    tesseract-ocr-deu \
    tesseract-ocr-div \
    tesseract-ocr-dzo \
    tesseract-ocr-ell \
    tesseract-ocr-eng \
    tesseract-ocr-enm \
    tesseract-ocr-epo \
    tesseract-ocr-est \
    tesseract-ocr-eus \
    tesseract-ocr-fao \
    tesseract-ocr-fas \
    tesseract-ocr-fil \
    tesseract-ocr-fin \
    tesseract-ocr-fra \
    tesseract-ocr-frk \
    tesseract-ocr-frm \
    tesseract-ocr-fry \
    tesseract-ocr-gla \
    tesseract-ocr-gle \
    tesseract-ocr-glg \
    tesseract-ocr-grc \
    tesseract-ocr-guj \
    tesseract-ocr-hat \
    tesseract-ocr-heb \
    tesseract-ocr-hin \
    tesseract-ocr-hrv \
    tesseract-ocr-hun \
    tesseract-ocr-hye \
    tesseract-ocr-iku \
    tesseract-ocr-ind \
    tesseract-ocr-isl \
    tesseract-ocr-ita \
    tesseract-ocr-ita-old \
    tesseract-ocr-jav \
    tesseract-ocr-jpn \
    tesseract-ocr-jpn-vert \
    tesseract-ocr-kan \
    tesseract-ocr-kat \
    tesseract-ocr-kat-old \
    tesseract-ocr-kaz \
    tesseract-ocr-khm \
    tesseract-ocr-kir \
    tesseract-ocr-kmr \
    tesseract-ocr-kor \
    tesseract-ocr-kor-vert \
    tesseract-ocr-lao \
    tesseract-ocr-lat \
    tesseract-ocr-lav \
    tesseract-ocr-lit \
    tesseract-ocr-ltz \
    tesseract-ocr-mal \
    tesseract-ocr-mar \
    tesseract-ocr-mkd \
    tesseract-ocr-mlt \
    tesseract-ocr-mon \
    tesseract-ocr-mri \
    tesseract-ocr-msa \
    tesseract-ocr-mya \
    tesseract-ocr-nep \
    tesseract-ocr-nld \
    tesseract-ocr-nor \
    tesseract-ocr-oci \
    tesseract-ocr-ori \
    tesseract-ocr-osd \
    tesseract-ocr-pan \
    tesseract-ocr-pol \
    tesseract-ocr-por \
    tesseract-ocr-pus \
    tesseract-ocr-que \
    tesseract-ocr-ron \
    tesseract-ocr-rus \
    tesseract-ocr-san \
    tesseract-ocr-script-arab \
    tesseract-ocr-script-armn \
    tesseract-ocr-script-beng \
    tesseract-ocr-script-cans \
    tesseract-ocr-script-cher \
    tesseract-ocr-script-cyrl \
    tesseract-ocr-script-deva \
    tesseract-ocr-script-ethi \
    tesseract-ocr-script-frak \
    tesseract-ocr-script-geor \
    tesseract-ocr-script-grek \
    tesseract-ocr-script-gujr \
    tesseract-ocr-script-guru \
    tesseract-ocr-script-hang \
    tesseract-ocr-script-hang-vert \
    tesseract-ocr-script-hans \
    tesseract-ocr-script-hans-vert \
    tesseract-ocr-script-hant \
    tesseract-ocr-script-hant-vert \
    tesseract-ocr-script-hebr \
    tesseract-ocr-script-jpan \
    tesseract-ocr-script-jpan-vert \
    tesseract-ocr-script-khmr \
    tesseract-ocr-script-knda \
    tesseract-ocr-script-laoo \
    tesseract-ocr-script-latn \
    tesseract-ocr-script-mlym \
    tesseract-ocr-script-mymr \
    tesseract-ocr-script-orya \
    tesseract-ocr-script-sinh \
    tesseract-ocr-script-syrc \
    tesseract-ocr-script-taml \
    tesseract-ocr-script-telu \
    tesseract-ocr-script-thaa \
    tesseract-ocr-script-thai \
    tesseract-ocr-script-tibt \
    tesseract-ocr-script-viet \
    tesseract-ocr-sin \
    tesseract-ocr-slk \
    tesseract-ocr-slv \
    tesseract-ocr-snd \
    tesseract-ocr-spa \
    tesseract-ocr-spa-old \
    tesseract-ocr-sqi \
    tesseract-ocr-srp \
    tesseract-ocr-srp-latn \
    tesseract-ocr-sun \
    tesseract-ocr-swa \
    tesseract-ocr-swe \
    tesseract-ocr-syr \
    tesseract-ocr-tam \
    tesseract-ocr-tat \
    tesseract-ocr-tel \
    tesseract-ocr-tgk \
    tesseract-ocr-tha \
    tesseract-ocr-tir \
    tesseract-ocr-ton \
    tesseract-ocr-tur \
    tesseract-ocr-uig \
    tesseract-ocr-ukr \
    tesseract-ocr-urd \
    tesseract-ocr-uzb \
    tesseract-ocr-uzb-cyrl \
    tesseract-ocr-vie \
    tesseract-ocr-yid \
    tesseract-ocr-yor \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements-base.txt /code/requirements-base.txt
COPY ./requirements-tesseract.txt /code/requirements-tesseract.txt
COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN if [ "$INSTALL_DEV" = "true" ]; then \
        pip install -r /code/requirements-dev.txt; \
    else \
        pip install -r /code/requirements-tesseract.txt; \
    fi

COPY . /code

WORKDIR /code

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.api:app"]


# =============================================================================
# Target: paddleocr (PaddleOCR only, Python 3.13)
# =============================================================================
FROM python:3.13-slim AS paddleocr

# Build argument to control whether to install dev dependencies
ARG INSTALL_DEV=false

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    FLASK_APP=app/api.py

RUN apt-get update && apt-get install -y \
    # Required for PaddleOCR
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements-base.txt /code/requirements-base.txt
COPY ./requirements-paddleocr-py313.txt /code/requirements-paddleocr-py313.txt
COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN if [ "$INSTALL_DEV" = "true" ]; then \
        pip install -r /code/requirements-dev.txt; \
    else \
        pip install -r /code/requirements-paddleocr-py313.txt; \
    fi

# Pre-download PaddleOCR models during build to avoid first-request delays
# NOTE: Additional models could be added here, or an initialization step could
# be implemented to download models after container startup.
RUN python3 -c "from paddleocr import PaddleOCR; PaddleOCR(use_angle_cls=True, lang='en', show_log=False)"

COPY . /code

WORKDIR /code

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.api:app"]


# =============================================================================
# Target: all (Both Tesseract and PaddleOCR, Python 3.12) - DEFAULT
# =============================================================================
FROM python:3.12-slim AS all

# Build argument to control whether to install dev dependencies
ARG INSTALL_DEV=false

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    FLASK_APP=app/api.py

# For a list of available Tesseract language packs, see:
# https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html

RUN apt-get update && apt-get install -y \
    # Required for PaddleOCR
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    # Tesseract OCR and language packs
    tesseract-ocr \
    tesseract-ocr-afr \
    tesseract-ocr-all \
    tesseract-ocr-amh \
    tesseract-ocr-ara \
    tesseract-ocr-asm \
    tesseract-ocr-aze \
    tesseract-ocr-aze-cyrl \
    tesseract-ocr-bel \
    tesseract-ocr-ben \
    tesseract-ocr-bod \
    tesseract-ocr-bos \
    tesseract-ocr-bre \
    tesseract-ocr-bul \
    tesseract-ocr-cat \
    tesseract-ocr-ceb \
    tesseract-ocr-ces \
    tesseract-ocr-chi-sim \
    tesseract-ocr-chi-sim-vert \
    tesseract-ocr-chi-tra \
    tesseract-ocr-chi-tra-vert \
    tesseract-ocr-chr \
    tesseract-ocr-cos \
    tesseract-ocr-cym \
    tesseract-ocr-dan \
    tesseract-ocr-deu \
    tesseract-ocr-div \
    tesseract-ocr-dzo \
    tesseract-ocr-ell \
    tesseract-ocr-eng \
    tesseract-ocr-enm \
    tesseract-ocr-epo \
    tesseract-ocr-est \
    tesseract-ocr-eus \
    tesseract-ocr-fao \
    tesseract-ocr-fas \
    tesseract-ocr-fil \
    tesseract-ocr-fin \
    tesseract-ocr-fra \
    tesseract-ocr-frk \
    tesseract-ocr-frm \
    tesseract-ocr-fry \
    tesseract-ocr-gla \
    tesseract-ocr-gle \
    tesseract-ocr-glg \
    tesseract-ocr-grc \
    tesseract-ocr-guj \
    tesseract-ocr-hat \
    tesseract-ocr-heb \
    tesseract-ocr-hin \
    tesseract-ocr-hrv \
    tesseract-ocr-hun \
    tesseract-ocr-hye \
    tesseract-ocr-iku \
    tesseract-ocr-ind \
    tesseract-ocr-isl \
    tesseract-ocr-ita \
    tesseract-ocr-ita-old \
    tesseract-ocr-jav \
    tesseract-ocr-jpn \
    tesseract-ocr-jpn-vert \
    tesseract-ocr-kan \
    tesseract-ocr-kat \
    tesseract-ocr-kat-old \
    tesseract-ocr-kaz \
    tesseract-ocr-khm \
    tesseract-ocr-kir \
    tesseract-ocr-kmr \
    tesseract-ocr-kor \
    tesseract-ocr-kor-vert \
    tesseract-ocr-lao \
    tesseract-ocr-lat \
    tesseract-ocr-lav \
    tesseract-ocr-lit \
    tesseract-ocr-ltz \
    tesseract-ocr-mal \
    tesseract-ocr-mar \
    tesseract-ocr-mkd \
    tesseract-ocr-mlt \
    tesseract-ocr-mon \
    tesseract-ocr-mri \
    tesseract-ocr-msa \
    tesseract-ocr-mya \
    tesseract-ocr-nep \
    tesseract-ocr-nld \
    tesseract-ocr-nor \
    tesseract-ocr-oci \
    tesseract-ocr-ori \
    tesseract-ocr-osd \
    tesseract-ocr-pan \
    tesseract-ocr-pol \
    tesseract-ocr-por \
    tesseract-ocr-pus \
    tesseract-ocr-que \
    tesseract-ocr-ron \
    tesseract-ocr-rus \
    tesseract-ocr-san \
    tesseract-ocr-script-arab \
    tesseract-ocr-script-armn \
    tesseract-ocr-script-beng \
    tesseract-ocr-script-cans \
    tesseract-ocr-script-cher \
    tesseract-ocr-script-cyrl \
    tesseract-ocr-script-deva \
    tesseract-ocr-script-ethi \
    tesseract-ocr-script-frak \
    tesseract-ocr-script-geor \
    tesseract-ocr-script-grek \
    tesseract-ocr-script-gujr \
    tesseract-ocr-script-guru \
    tesseract-ocr-script-hang \
    tesseract-ocr-script-hang-vert \
    tesseract-ocr-script-hans \
    tesseract-ocr-script-hans-vert \
    tesseract-ocr-script-hant \
    tesseract-ocr-script-hant-vert \
    tesseract-ocr-script-hebr \
    tesseract-ocr-script-jpan \
    tesseract-ocr-script-jpan-vert \
    tesseract-ocr-script-khmr \
    tesseract-ocr-script-knda \
    tesseract-ocr-script-laoo \
    tesseract-ocr-script-latn \
    tesseract-ocr-script-mlym \
    tesseract-ocr-script-mymr \
    tesseract-ocr-script-orya \
    tesseract-ocr-script-sinh \
    tesseract-ocr-script-syrc \
    tesseract-ocr-script-taml \
    tesseract-ocr-script-telu \
    tesseract-ocr-script-thaa \
    tesseract-ocr-script-thai \
    tesseract-ocr-script-tibt \
    tesseract-ocr-script-viet \
    tesseract-ocr-sin \
    tesseract-ocr-slk \
    tesseract-ocr-slv \
    tesseract-ocr-snd \
    tesseract-ocr-spa \
    tesseract-ocr-spa-old \
    tesseract-ocr-sqi \
    tesseract-ocr-srp \
    tesseract-ocr-srp-latn \
    tesseract-ocr-sun \
    tesseract-ocr-swa \
    tesseract-ocr-swe \
    tesseract-ocr-syr \
    tesseract-ocr-tam \
    tesseract-ocr-tat \
    tesseract-ocr-tel \
    tesseract-ocr-tgk \
    tesseract-ocr-tha \
    tesseract-ocr-tir \
    tesseract-ocr-ton \
    tesseract-ocr-tur \
    tesseract-ocr-uig \
    tesseract-ocr-ukr \
    tesseract-ocr-urd \
    tesseract-ocr-uzb \
    tesseract-ocr-uzb-cyrl \
    tesseract-ocr-vie \
    tesseract-ocr-yid \
    tesseract-ocr-yor \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
COPY ./requirements-base.txt /code/requirements-base.txt
COPY ./requirements-tesseract.txt /code/requirements-tesseract.txt
COPY ./requirements-paddleocr.txt /code/requirements-paddleocr.txt
COPY ./requirements-dev.txt /code/requirements-dev.txt

RUN if [ "$INSTALL_DEV" = "true" ]; then \
        pip install -r /code/requirements-dev.txt; \
    else \
        pip install -r /code/requirements.txt; \
    fi

# Pre-download PaddleOCR models during build to avoid first-request delays
# NOTE: Additional models could be added here, or an initialization step could
# be implemented to download models after container startup.
RUN python3 -c "from paddleocr import PaddleOCR; PaddleOCR(use_angle_cls=True, lang='en', show_log=False)"

COPY . /code

WORKDIR /code

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.api:app"]
