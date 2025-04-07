FROM bitnami/spark:3.3.0

# Set working directory inside the container
WORKDIR /app

# Copy local contents (context starts from spark_streaming/)
COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/
COPY resources/schemas/ ./resources/schemas/

# Install additional Python packages if needed
USER root
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install pandas requests

# Spark packages for Kafka + Delta
ENV SPARK_PACKAGES=org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.0.0

# Set entrypoint to run Spark job
ENTRYPOINT [ "/opt/bitnami/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py" ]
