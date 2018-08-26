FROM ubuntu:17.10

ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=app/api.py

RUN apt-get update && apt-get install -y software-properties-common curl && add-apt-repository -y ppa:alex-p/tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY . /code

WORKDIR /code

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
