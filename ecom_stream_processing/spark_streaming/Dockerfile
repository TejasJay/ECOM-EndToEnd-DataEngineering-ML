# syntax=docker/dockerfile:1.4
FROM bitnami/spark:3.3.0

WORKDIR /app

COPY requirements.txt .
USER root
RUN apt-get update && apt-get install -y python3-pip && pip install --no-cache-dir -r requirements.txt

# 🧠 Prefetch Spark packages to avoid Ivy delay at runtime
RUN /opt/bitnami/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.kafka:kafka-clients:2.8.0,io.delta:delta-core_2.12:2.0.0 \
  --dry-run \
  > /dev/null 2>&1 || true

COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/
COPY resources/ ./resources/


ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.kafka:kafka-clients:2.8.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py"]
