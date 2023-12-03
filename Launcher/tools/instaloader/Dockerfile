# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /app

COPY . .

RUN python3 -m pip install requests
RUN chmod +x ./instaloader.py
