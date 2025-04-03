# 🐳 Kafka Ingestion Layer Makefile
-include .env.secrets

COMPOSE=docker-compose
PYTHON=python3
PROJECT_DIR=$(shell pwd)
TOPIC?=users

.PHONY: help start stop restart logs status create-topics consume produce

# 🔹 Show help menu
help:
	@echo "Kafka Ingestion Layer Commands:"
	@echo ""
	@echo "  make start              - Start Kafka + Zookeeper"
	@echo "  make stop               - Stop all containers"
	@echo "  make restart            - Restart Kafka stack"
	@echo "  make logs               - View live Kafka logs"
	@echo "  make status             - Show container status"
	@echo "  make create-topics      - Run the topic creation script"
	@echo "  make consume-topic      - Run test Kafka consumer (requires TOPIC=...)"
	@echo "  make produce-topic      - Run test Kafka producer (requires TOPIC=...)"
	@echo "  make ps                 - Alias for docker-compose ps"
	@echo "  make nuke               - Remove all containers, volumes, and networks 💣"

login:
	docker login -u $(DOCKERHUB_USERNAME) -p $(DOCKERHUB_PASSWORD)

# 🔹 Start Kafka and Zookeeper
start:
	@echo "🚀 Starting Kafka stack..."
	$(COMPOSE) up -d

# 🔹 Stop Kafka and Zookeeper
stop:
	@echo "🛑 Stopping Kafka stack..."
	$(COMPOSE) down

# 🔹 Stop and remove all containers + volumes
nuke:
	@echo "💣 Stopping and removing containers, volumes, and networks..."
	$(COMPOSE) down -v

# 🔹 Restart containers
restart: stop start

# 🔹 Tail logs
logs:
	@echo "📜 Showing Kafka logs..."
	$(COMPOSE) logs -f kafka

# 🔹 Show container status
status ps:
	@echo "📦 Kafka container status:"
	$(COMPOSE) ps

build-topics:
	@echo "🐳 Building Docker image for topic creation..."
	docker build -t ecom_create_topics:latest ./topics

push-topics: build-topics
	docker tag ecom_create_topics:latest tejasjay03/ecom_create_topics:latest
	docker push tejasjay03/ecom_create_topics:latest

create-topics:
	@echo "🧱 Creating Kafka topics via Docker container..."
	docker run --rm --network kafka_kafka_net ecom_create_topics:latest

# 🔹 Run Kafka Consumer for a specific topic
consume-topic:
	@echo "📥 Consuming from topic: $(TOPIC)"
	$(PYTHON) consumer/test_consumer.py --topic $(TOPIC)

build-consumer:
	@echo "🐳 Building Kafka consumer image..."
	docker build -t ecom_kafka_consumer:latest ./consumer

push-consumer: build-consumer
	docker tag ecom_kafka_consumer:latest  tejasjay03/ecom_kafka_consumer:latest 
	docker push tejasjay03/ecom_kafka_consumer:latest 

# 🔹 Run Kafka Consumer Container
run-consumer:
	@echo "📦 Running Kafka consumer container..."
	docker run --rm --network kafka_kafka_net ecom_kafka_consumer:latest



bootstrap: start build-topics create-topics build-consumer run-consumer
