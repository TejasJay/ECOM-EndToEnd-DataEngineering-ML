import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, from_json

# Load YAML config
with open("config/streaming_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Config values
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

# Define the user schema inline
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
    StructField("account_creation_date", TimestampType()),
    StructField("last_login_time", TimestampType()),
    StructField("preferred_language", StringType()),
    StructField("persona", StringType())
])

# Read from Kafka topic
users_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", brokers) \
    .option("subscribe", user_topic) \
    .option("startingOffsets", starting_offsets) \
    .load()

# Parse and extract fields
users_parsed = users_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), user_schema).alias("data")) \
    .select("data.*")

# Output to console
print("✅ Starting user stream...")
users_query = users_parsed.writeStream \
    .format("console") \
    .outputMode(output_mode) \
    .option("truncate", truncate) \
    .queryName("UserStream") \
    .start()

# Await termination
spark.streams.awaitAnyTermination()
