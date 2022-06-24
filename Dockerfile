# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install vim -y \
    && pip install --upgrade pip && pip3 install -r requirements.txt

COPY . /code/