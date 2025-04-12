import yaml
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
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
user_schema_path = config["schema"]["user_schema_path"]

print(f"🧪 Kafka brokers being used: {brokers}")
print(f"📡 Subscribing to topic: {user_topic}")
print(f"⏳ Starting offset: {starting_offsets}")

# Initialize Spark
spark = SparkSession.builder.appName(app_name).getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Load user schema from JSON
with open(user_schema_path, "r") as f:
    user_schema_json = json.load(f)

user_schema = StructType.fromJson(user_schema_json)

# Read user stream
users_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", brokers) \
    .option("subscribe", user_topic) \
    .option("startingOffsets", starting_offsets) \
    .load()

# Parse Kafka JSON messages
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

spark.streams.awaitAnyTermination()
