FROM python:3.10.6

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt 
RUN pip install flake8 flake8-docstrings restructuredtext-lint


COPY . .
