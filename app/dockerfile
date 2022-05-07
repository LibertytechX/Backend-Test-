FROM python:3.8.12-alpine
LABEL Inyang Kpongette

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r /requirements.txt \
    && apk del .build-deps
RUN pip install flake8 flake8-docstrings restructuredtext-lint
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user