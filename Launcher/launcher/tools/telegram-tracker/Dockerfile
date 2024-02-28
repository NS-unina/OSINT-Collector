# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

RUN git clone https://github.com/estebanpdl/telegram-api.git .

COPY session_file.session session_file.session
COPY config.ini config/config.ini

RUN python3 -m pip install -r requirements.txt