import yaml
import os

# Load YAML config
with open("config/streaming_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Extract config values
app_name = config["app_name"]
brokers = config["kafka"]["brokers"]
topic = config["kafka"]["topic"]
starting_offsets = config["kafka"]["starting_offsets"]
output_mode = config["output"]["mode"]
truncate = config["output"]["truncate"]

# Spark session
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName(app_name).getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Define schema (you can also load it from JSON later)
from pyspark.sql.types import *
transaction_schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("user_id", StringType()) \
    .add("item_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("timestamp", TimestampType())

# Read from Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", brokers) \
    .option("subscribe", topic) \
    .option("startingOffsets", starting_offsets) \
    .load()

# Parse JSON messages
from pyspark.sql.functions import col, from_json
parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), transaction_schema).alias("data")) \
    .select("data.*")

# Output to console (from config)
query = parsed.writeStream \
    .format(output_mode) \
    .option("truncate", truncate) \
    .start()

query.awaitTermination()
