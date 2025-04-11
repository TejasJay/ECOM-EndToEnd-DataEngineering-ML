# syntax=docker/dockerfile:1.4
FROM bitnami/spark:3.3.0

WORKDIR /app

COPY requirements.txt .

USER root

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt

# Pre-fetch Spark packages using dry-run (ignore failure)
RUN /opt/bitnami/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.kafka:kafka-clients:2.8.0,io.delta:delta-core_2.12:2.0.0 \
  --dry-run || true

# ✅ If Ivy cache exists, copy it — but don’t crash if it doesn't
RUN mkdir -p /ivy_cache && \
    if [ -d /root/.ivy2 ]; then cp -r /root/.ivy2 /ivy_cache; else echo "No Ivy cache found, continuing..."; fi

# Copy your code and configs
COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/
COPY resources/ ./resources/

# Restore cached Ivy jars (safe even if it didn’t exist)
RUN if [ -d /ivy_cache/.ivy2 ]; then cp -r /ivy_cache/.ivy2 /root/; fi

ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.kafka:kafka-clients:2.8.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py"]
