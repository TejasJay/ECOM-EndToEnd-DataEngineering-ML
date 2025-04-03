from kafka import KafkaConsumer
import orjson
import argparse
import socket

def get_bootstrap_host():
    try:
        socket.gethostbyname("kafka")  # Inside Docker network
        return "kafka:9092"
    except socket.error:
        return "localhost:9092"  # Fallback for local host runs

BROKER_URL = get_bootstrap_host()

def main():
    parser = argparse.ArgumentParser(description="Kafka Consumer for Testing Topics")
    parser.add_argument("--topic", type=str, default="users")
    parser.add_argument("--bootstrap", type=str, default=BROKER_URL)
    parser.add_argument("--group", type=str, default="test-consumer-group")
    args = parser.parse_args()

    print(f"🔄 Connecting to Kafka topic '{args.topic}' on {args.bootstrap}...")

    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=args.bootstrap,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=args.group,
        value_deserializer=lambda m: orjson.loads(m),
    )

    print(f"✅ Listening for messages on topic: {args.topic}...")
    try:
        for message in consumer:
            print("📥 Received message:")
            print(message.value)
    except KeyboardInterrupt:
        print("\n🛑 Exiting...")
    finally:
        consumer.close()
        print("🔌 Consumer connection closed.")

if __name__ == "__main__":
    main()
