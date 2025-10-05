# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

RUN git clone https://github.com/instaloader/instaloader.git --branch v4.10.2 .

RUN python3 -m pip install requests
RUN chmod +x ./instaloader.py
