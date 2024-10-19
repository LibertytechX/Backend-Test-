FROM python:3.11.7-alpine

LABEL maintainer="ayobamidele006@gmail.com"

WORKDIR /app

COPY . /app

RUN apk add --virtual .build-deps gcc musl-dev \
    && pip install -r ./requirements.txt \
    && apk del .build-deps

# EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:80"]