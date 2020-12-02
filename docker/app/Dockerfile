FROM python:3.7-alpine as base
FROM base as builder
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
