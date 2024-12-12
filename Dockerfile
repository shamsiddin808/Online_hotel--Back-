FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the port 8000 for Django
EXPOSE 8000
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt