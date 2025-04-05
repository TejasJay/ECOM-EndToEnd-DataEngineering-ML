from kafka import KafkaConsumer
import socket
import json

# Determine Kafka broker address (inside Docker uses "kafka", outside uses localhost)
def get_bootstrap_host():
    try:
        socket.gethostbyname("kafka")
        return "kafka:29092"
    except socket.error:
        return "localhost:9092"

BOOTSTRAP_SERVERS = get_bootstrap_host()
TOPIC = "users"
GROUP_ID = "test-consumer-group"

def main():
    print(f"🔄 Connecting to Kafka topic '{TOPIC}' on {BOOTSTRAP_SERVERS}....")

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print(f"✅ Listening for messages on topic: {TOPIC}...")
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
