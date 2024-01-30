# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

COPY . .

RUN python3 -m pip install -r requirements.txt
RUN chmod +x ./main.py
CMD "./main.py"