import yaml
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, from_json

# Load YAML config
with open("config/streaming_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Extract config values
app_name = config["app_name"]
brokers = config["kafka"]["brokers"]
user_topic = config["kafka"]["topics"]["users"]
starting_offsets = config["kafka"]["starting_offsets"]
output_mode = config["output"]["mode"]
truncate = config["output"]["truncate"]

print(f"🧪 Kafka brokers being used: {brokers}")
print(f"📡 Subscribing to topic: {user_topic}")
print(f"⏳ Starting offset: {starting_offsets}")

# Initialize Spark session
spark = SparkSession.builder.appName(app_name).getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Load user schema from JSON file
user_schema_path = config["schema"]["user_schema_path"]
with open(user_schema_path, "r") as f:
    user_schema_json = json.load(f)

# Convert JSON Schema to StructType (manual mapping)
user_schema = StructType([
    StructField("user_id", StringType()),
    StructField("first_name", StringType()),
    StructField("last_name", StringType()),
    StructField("user_name", StringType()),
    StructField("user_type", StringType()),
    StructField("age_group", StringType()),
    StructField("gender", StringType()),
    StructField("address", StringType()),
    StructField("city", StringType()),
    StructField("state", StringType()),
    StructField("zipcode", StringType()),
    StructField("country", StringType()),
    StructField("account_creation_date", StringType()),  # relaxed from TimestampType
    StructField("last_login_time", StringType()),        # relaxed from TimestampType
    StructField("preferred_language", StringType()),
    StructField("persona", StringType())
])

# Read stream from Kafka
users_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", brokers) \
    .option("subscribe", user_topic) \
    .option("startingOffsets", starting_offsets) \
    .option("failOnDataLoss", "false") \
    .load()

# 1️⃣ DEBUG: Raw Kafka messages
raw_query = users_df.selectExpr("CAST(value AS STRING) AS raw_value") \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .queryName("RawKafkaOutput") \
    .start()

# 2️⃣ Parse messages from JSON
parsed_users = users_df.selectExpr("CAST(value AS STRING) AS json_str") \
    .select(from_json(col("json_str"), user_schema).alias("data")) \
    .select("data.*")

# 3️⃣ DEBUG: Print null (bad) records
malformed_query = parsed_users.filter(col("user_id").isNull()) \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .queryName("MalformedUsers") \
    .start()

# 4️⃣ Main user stream output
print("✅ Starting user stream...")
valid_users_query = parsed_users.filter(col("user_id").isNotNull()) \
    .writeStream \
    .format("console") \
    .outputMode(output_mode) \
    .option("truncate", truncate) \
    .queryName("UserStream") \
    .start()

# Await termination of all queries
spark.streams.awaitAnyTermination()
