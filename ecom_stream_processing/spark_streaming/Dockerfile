# syntax=docker/dockerfile:1.4

# 🐳 Base Image: Bitnami Spark includes Spark, Hadoop, Python
FROM bitnami/spark:3.3.0

# Set working directory inside container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
USER root
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code and configuration
COPY streaming_jobs/ ./streaming_jobs/

# 🧠 Run Spark Streaming job with packages auto-resolved at runtime
ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.kafka:kafka-clients:2.8.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py"]
