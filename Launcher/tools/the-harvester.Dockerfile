# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

ADD https://github.com/laramies/theHarvester.git#4.4.4 .

RUN python3 -m pip install -r requirements.txt

