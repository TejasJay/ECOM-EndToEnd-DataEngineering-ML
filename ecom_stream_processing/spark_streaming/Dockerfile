# Use Bitnami Spark base image
FROM bitnami/spark:3.3.0

# Enable platform override for Mac M1 users
ARG TARGETPLATFORM

# Set working directory inside container
WORKDIR /app

# Copy app code, config, and schemas into container
COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/

# Install Python packages
USER root
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install pandas requests pyyaml

# Spark packages: Kafka connector and Delta Lake support
ENV SPARK_PACKAGES=org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.0.0

# Entrypoint to run the streaming job
ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.0.0", \
  "/app/streaming_jobs/enrich_transaction.py"]
