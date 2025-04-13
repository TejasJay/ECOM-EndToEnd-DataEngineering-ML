from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import *

# Inline schema from simulation
schema = StructType([
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
    StructField("account_creation_date", StringType()),
    StructField("last_login_time", StringType()),
    StructField("preferred_language", StringType()),
    StructField("persona", StringType())
])

kafka_bootstrap = "kafka:29092"
input_topic = "users"
output_topic = "filtered_users"

print(f"🧪 Kafka brokers: {kafka_bootstrap}")
print(f"📡 Reading topic: {input_topic} → Writing to: {output_topic}")

spark = SparkSession.builder.appName("UserEnrichmentStream").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

raw_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap) \
    .option("subscribe", input_topic) \
    .option("startingOffsets", "earliest") \
    .option("kafka.group.id", "spark-streaming-group") \
    .load()

parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("account_creation_date", to_timestamp("account_creation_date")) \
    .withColumn("last_login_time", to_timestamp("last_login_time"))

# Filter condition - you can tweak or comment
filtered_df = parsed_df.filter(col("country") == "USA")

# Write to Kafka
filtered_df.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap) \
    .option("topic", output_topic) \
    .option("checkpointLocation", "/tmp/spark-checkpoint-users") \
    .outputMode("append") \
    .start()

# Write to Console
filtered_df.writeStream \
    .format("console") \
    .option("truncate", False) \
    .option("numRows", 5) \
    .outputMode("append") \
    .start()

print("🚀 Spark streaming started. Waiting for data...")
spark.streams.awaitAnyTermination()
