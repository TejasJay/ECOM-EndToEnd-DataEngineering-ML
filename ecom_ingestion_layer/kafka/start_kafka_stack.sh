#!/bin/bash

set -e  # Exit on error
set -u  # Treat unset vars as error

echo "🔁 Restarting Kafka & Zookeeper..."
make restart

echo "⏳ Waiting for Kafka to be ready (sleeping for 10s)..."
sleep 20

echo "🧱 Creating required Kafka topics..."
make create-topics

sleep 10

echo "✅ Kafka ingestion stack is ready!"

sleep 5

echo "✅✅✅✅✅✅✅✅ Consuming!!!!!!!!!"



