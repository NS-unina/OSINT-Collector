# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

RUN git clone https://github.com/ciro-99/blackbird.git .

RUN python3 -m pip install -r requirements.txt
RUN chmod +x ./blackbird.py