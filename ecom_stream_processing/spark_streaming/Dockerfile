# syntax=docker/dockerfile:1.4
FROM bitnami/spark:3.3.0

WORKDIR /app

COPY requirements.txt .
USER root

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt

COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/
COPY resources/ ./resources
COPY jars/ ./jars/

ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--jars", "/app/jars/spark-sql-kafka-0-10_2.12-3.3.0.jar,/app/jars/spark-token-provider-kafka-0-10_2.12-3.3.0.jar,/app/jars/delta-core_2.12-2.0.0.jar", \
  "/app/streaming_jobs/enrich_transaction.py"]
