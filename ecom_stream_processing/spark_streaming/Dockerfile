# syntax=docker/dockerfile:1.4
FROM --platform=linux/amd64 bitnami/spark:3.3.0

# Switch to root for installing system packages
USER root

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .

RUN apt-get clean && \
    apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code (your Spark script)
COPY streaming_jobs/ ./streaming_jobs/
