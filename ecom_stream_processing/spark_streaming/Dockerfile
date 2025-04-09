# syntax=docker/dockerfile:1.4

# Use Bitnami Spark (includes Spark, Hadoop, Python)
FROM bitnami/spark:3.3.0

ARG TARGETPLATFORM

# Set working directory
WORKDIR /app

# Copy requirements separately to leverage caching.
COPY requirements.txt .

USER root

# Install Python dependencies cleanly
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your code and config
COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/

# Run the Spark Streaming job with necessary packages
ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py"]
