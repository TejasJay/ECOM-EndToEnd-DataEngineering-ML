#!/bin/sh

KAFKA_HOST=$1
KAFKA_PORT=$2

echo "⏳ Waiting for Kafka to be ready at $KAFKA_HOST:$KAFKA_PORT..."

while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
  echo "❌ Kafka not ready yet..."
  sleep 2
done

echo "✅ Kafka is up!"
exec "${@:3}"  # run the command passed after host and port
