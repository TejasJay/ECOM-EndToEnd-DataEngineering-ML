import yaml
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.functions import col, from_json, to_timestamp

# Load config
with open("config/streaming_config.yaml", "r") as f:
    config = yaml.safe_load(f)

app_name = config["app_name"]
brokers = config["kafka"]["brokers"]
user_topic = config["kafka"]["topics"]["users"]
starting_offsets = config["kafka"]["starting_offsets"]
output_mode = config["output"]["mode"]
truncate = config["output"]["truncate"]
user_schema_path = config["schema"]["user_schema_path"]

print(f"🧪 Kafka brokers being used: {brokers}")
print(f"📡 Subscribing to topic: {user_topic}")
print(f"⏳ Starting offset: {starting_offsets}")

# Load schema
with open(user_schema_path, "r") as f:
    user_schema_json = json.load(f)

user_schema = StructType.fromJson(user_schema_json)

# Create Spark session
spark = SparkSession.builder.appName(app_name).getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Read Kafka stream
users_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", brokers) \
    .option("subscribe", user_topic) \
    .option("startingOffsets", starting_offsets) \
    .load()

# Parse value
users_parsed = users_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), user_schema).alias("data")) \
    .select("data.*") \
    .withColumn("account_creation_date", to_timestamp("account_creation_date")) \
    .withColumn("last_login_time", to_timestamp("last_login_time"))

# Write to console
print("✅ Starting user stream...")
users_query = users_parsed.writeStream \
    .format("console") \
    .outputMode(output_mode) \
    .option("truncate", truncate) \
    .option("numRows", 5) \
    .queryName("UserStream") \
    .start()

spark.streams.awaitAnyTermination()
