# syntax=docker/dockerfile:1.4

# ✅ Base image with Spark, Hadoop, and Python
FROM bitnami/spark:3.3.0

WORKDIR /app

# 📦 Copy Python requirements first for caching
COPY requirements.txt .

# 👑 Switch to root for installing pip + dependencies
USER root

# ✅ Install Python packages
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt

# ⚡ Pre-download Spark packages using --dry-run (cached by Ivy)
RUN /opt/bitnami/spark/bin/spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.kafka:kafka-clients:2.8.0,io.delta:delta-core_2.12:2.0.0 \
    --dry-run || true

# 🧊 Cache Ivy jars for future layers
RUN mkdir -p /ivy_cache && cp -r /root/.ivy2 /ivy_cache

# 🔁 Copy your code and config
COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/
COPY resources/ ./resources/

# 🔁 Restore Ivy cache at runtime to skip repeated downloads
RUN cp -r /ivy_cache/.ivy2 /root/

# ✅ Set entrypoint to run your streaming job
ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.kafka:kafka-clients:2.8.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py"]
