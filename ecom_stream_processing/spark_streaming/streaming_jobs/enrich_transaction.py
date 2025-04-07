from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

# Step 1: Create Spark Session
spark = SparkSession.builder \
    .appName("EnrichTransactionStream") \
    .getOrCreate()

# Optional: Set log level to reduce noise
spark.sparkContext.setLogLevel("WARN")

# Step 2: Define schema for transaction events
transaction_schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("user_id", StringType()) \
    .add("item_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("timestamp", TimestampType())

# Step 3: Read streaming data from Kafka topic
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "pos_transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Step 4: Decode Kafka value column and apply schema
parsed_df = raw_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), transaction_schema).alias("data")) \
    .select("data.*")

# Step 5: Write the stream to console (testing phase)
query = parsed_df.writeStream \
    .format("console") \
    .option("truncate", False) \
    .outputMode("append") \
    .start()

# Step 6: Keep the stream running
query.awaitTermination()

