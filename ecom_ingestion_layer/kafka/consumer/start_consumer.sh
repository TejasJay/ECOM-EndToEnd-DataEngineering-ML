#!/bin/bash
set -e

KAFKA_HOST="${BOOTSTRAP:-host.docker.internal:9092}"
TOPIC="${TOPIC:-users}"

HOST=$(echo "$KAFKA_HOST" | cut -d: -f1)
PORT=$(echo "$KAFKA_HOST" | cut -d: -f2)

echo "⏳ Waiting for Kafka at $KAFKA_HOST..."

for i in {1..20}; do
  if nc -z "$HOST" "$PORT"; then
    echo "✅ Kafka is reachable"
    break
  fi
  echo "❌ Kafka not ready, retrying in 2s..."
  sleep 2
done

echo "📥 Starting Kafka consumer for topic: $TOPIC"
python3 test_consumer.py --topic "$TOPIC" --bootstrap "$KAFKA_HOST"
