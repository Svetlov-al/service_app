FROM python:3.9-alpine3.16
LABEL authors="aleksandr"

COPY requirements.txt /temp/requirements.txt
COPY service /service

WORKDIR /service
EXPOSE 8080


RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user
