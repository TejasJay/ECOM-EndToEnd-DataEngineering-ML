# syntax=docker/dockerfile:1.4

# Use Apache's official Spark + Python base image
FROM apache/spark-py:3.3.0

# Support for multi-arch builds (Mac M1 and Linux)
ARG TARGETPLATFORM

# Set working directory
WORKDIR /app

# Copy Python dependencies first to cache them
COPY requirements.txt .

USER root

# Install Python packages efficiently
RUN pip install --no-cache-dir -r requirements.txt

# Now copy source code and configs
COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/

# Default entrypoint
ENTRYPOINT ["/opt/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py"]
