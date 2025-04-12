# syntax=docker/dockerfile:1.4

# Use Bitnami Spark (includes Spark, Hadoop, and Python)
FROM bitnami/spark:3.3.0

ARG TARGETPLATFORM

# Set working directory
WORKDIR /app

# Install Python requirements cleanly
COPY requirements.txt .
USER root
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install --no-cache-dir -r requirements.txt

# Manually download and cache Kafka + Delta JARs (to avoid Ivy downloading at runtime)
RUN mkdir -p /app/jars && \
    curl -L -o /app/jars/spark-sql-kafka-0-10_2.12-3.3.0.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.3.0/spark-sql-kafka-0-10_2.12-3.3.0.jar && \
    curl -L -o /app/jars/spark-token-provider-kafka-0-10_2.12-3.3.0.jar https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.3.0/spark-token-provider-kafka-0-10_2.12-3.3.0.jar && \
    curl -L -o /app/jars/delta-core_2.12-2.0.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.0.0/delta-core_2.12-2.0.0.jar

# Copy app code and config
COPY streaming_jobs/ ./streaming_jobs/
COPY config/ ./config/

# Conditionally copy resources/ directory if it exists
RUN mkdir -p /app/resources
COPY resources/ ./resources/

# Add the jars directory to the Spark classpath
ENV SPARK_EXTRA_CLASSPATH=/app/jars/*

# Run the main Spark script
ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit", \
  "--jars", "/app/jars/spark-sql-kafka-0-10_2.12-3.3.0.jar,/app/jars/spark-token-provider-kafka-0-10_2.12-3.3.0.jar,/app/jars/delta-core_2.12-2.0.0.jar", \
  "/app/streaming_jobs/enrich_transaction.py"]
