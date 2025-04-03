## **📌 Separate Config Files**


## **🔧 Recommended File Structure**

📦 **kafka-configs/**
┣━━ 📝 **server.properties** _(Kafka broker config)_
┣━━ 📝 **producer.config** _(Producer-specific settings)_
┗━━ 📝 **consumer.config** _(Consumer-specific settings)_

* * *

## **🚀 Example: Producer Config (`producer.config`)**

```properties
bootstrap.servers=broker1:9092,broker2:9092  # Kafka broker addresses
acks=all  # Ensure strong durability
compression.type=snappy  # Compress messages for efficiency
batch.size=16384  # 16KB batch size
linger.ms=5  # Small delay for batching
max.request.size=10485760  # Max message size (10MB)
retries=5  # Retry on failure
```

-   **For large messages**, increase `max.request.size`.
-   **For high-throughput, optimize `batch.size` & `compression.type`.**
* * *

## **📥 Example: Consumer Config (`consumer.config`)**

```properties
bootstrap.servers=broker1:9092,broker2:9092  # Kafka broker addresses
group.id=my-consumer-group  # Consumer group ID
auto.offset.reset=earliest  # Start from the beginning if no offset is found
enable.auto.commit=false  # Avoid accidental commits
fetch.max.bytes=10485760  # Max data fetched per poll (10MB)
max.poll.records=500  # Limit number of records per fetch
session.timeout.ms=30000  # Consumer session timeout
```

-   **For small messages, decrease `fetch.max.bytes`.**
-   **For real-time low-latency processing, increase `max.poll.records`.**
* * *

## **🔗 How to Use These Config Files?**

Run Kafka producer/consumer **using the config files**:

```bash
# Start a producer using producer.config
kafka-console-producer.sh --topic my-topic --broker-list broker1:9092 --producer.config kafka-configs/producer.config

# Start a consumer using consumer.config
kafka-console-consumer.sh --topic my-topic --bootstrap-server broker1:9092 --consumer.config kafka-configs/consumer.config
```

* * *



