# syntax=docker/dockerfile:1

FROM python:3.9.23-slim

COPY ./new-Laucher/ /root/

WORKDIR /root/

RUN pip install --no-cache-dir -r requirements-test.txt