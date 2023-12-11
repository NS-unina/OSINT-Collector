# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

ADD https://github.com/instaloader/instaloader.git#v4.10.2 .

RUN python3 -m pip install requests
RUN chmod +x ./instaloader.py
