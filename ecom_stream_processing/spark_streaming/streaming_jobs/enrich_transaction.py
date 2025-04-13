from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import *
import uuid

# Define the schema inline (from your simulation structure)
user_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("user_name", StringType(), True),
    StructField("user_type", StringType(), True),
    StructField("age_group", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("zipcode", StringType(), True),
    StructField("country", StringType(), True),
    StructField("account_creation_date", StringType(), True),
    StructField("last_login_time", StringType(), True),
    StructField("preferred_language", StringType(), True),
    StructField("persona", StringType(), True)
])

# Kafka config
kafka_bootstrap = "kafka:29092"
input_topic = "users"
output_topic = "filtered_users"

print(f"🧪 Kafka brokers: {kafka_bootstrap}")
print(f"📡 Reading topic: {input_topic} → Writing to: {output_topic}")

# Start Spark session
spark = SparkSession.builder \
    .appName("UserEnrichmentStream") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Read from Kafka
raw_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap) \
    .option("subscribe", input_topic) \
    .option("startingOffsets", "earliest") \
    .load()

# Parse and flatten
parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), user_schema).alias("data")) \
    .select("data.*") \
    .withColumn("account_creation_date", to_timestamp("account_creation_date")) \
    .withColumn("last_login_time", to_timestamp("last_login_time"))

# Apply filter — you can comment this line out to test full flow
filtered_df = parsed_df

# Output to Kafka
kafka_out = filtered_df.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap) \
    .option("topic", output_topic) \
    .option("checkpointLocation", f"/tmp/spark_checkpoint_{uuid.uuid4()}") \
    .outputMode("append") \
    .start()

# Output to Console
console_out = filtered_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .option("numRows", 3) \
    .start()

# Start both streams
print("🚀 Spark streaming started. Waiting for data...")
spark.streams.awaitAnyTermination()
