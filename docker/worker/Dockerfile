FROM python:3.7-alpine as base
FROM base as builder
RUN mkdir /app
WORKDIR /app
COPY tasks.py .
COPY smc_tools.py .
COPY celeryconfig.py .
COPY requirements.txt .
COPY config.py .
RUN pip install --no-cache-dir -r requirements.txt