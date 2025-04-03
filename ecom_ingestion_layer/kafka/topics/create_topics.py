from confluent_kafka.admin import AdminClient, NewTopic
import socket

def get_bootstrap_host():
    try:
        socket.gethostbyname("kafka")  # Works inside Docker
        return "kafka:29092"
    except socket.error:
        print("⚠️ 'kafka' hostname not found. Falling back to localhost.")
        return "localhost:9092"

BROKER_URL = get_bootstrap_host()

# Topics to create
TOPICS = [
    "users",
    "sessions",
    "orders",
    "behaviours",
    "marketings"
]

NUM_PARTITIONS = 3
REPLICATION_FACTOR = 1

def create_topics():
    admin_client = AdminClient({"bootstrap.servers": BROKER_URL})
    print(f"📡 Connected to Kafka at {BROKER_URL}")

    # Fetch existing topics
    existing_topics = admin_client.list_topics(timeout=10).topics
    print(f"📚 Existing topics: {list(existing_topics.keys())}")

    topics_to_create = [
        topic for topic in TOPICS if topic not in existing_topics
    ]

    if not topics_to_create:
        print("✅ All desired topics already exist.")
        return

    # Build topic definitions
    new_topics = [
        NewTopic(topic, num_partitions=NUM_PARTITIONS, replication_factor=REPLICATION_FACTOR)
        for topic in topics_to_create
    ]

    print(f"🧱 Creating topics: {topics_to_create}")
    fs = admin_client.create_topics(new_topics)

    for topic, future in fs.items():
        try:
            future.result()
            print(f"✅ Created topic: {topic}")
        except Exception as e:
            print(f"❌ Failed to create topic '{topic}': {e}")

if __name__ == "__main__":
    create_topics()
