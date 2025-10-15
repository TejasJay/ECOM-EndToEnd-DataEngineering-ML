# Project settings
PROJECT_NAME=spark_streaming
SERVICE_NAME=spark-submit-job
DOCKER_COMPOSE=docker-compose.yml

# Build and bring up the full stack
up:
	@echo "🚀 Starting Spark + Kafka stack with streaming job..."
	DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose -f $(DOCKER_COMPOSE) up --build

# Rebuild the streaming job only (faster if only Python code changes)
rebuild:
	@echo "🔄 Rebuilding spark-submit-job image..."
	DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose -f $(DOCKER_COMPOSE) build $(SERVICE_NAME)

# Tail logs from the streaming job
logs:
	@echo "📜 Showing logs for $(SERVICE_NAME)..."
	docker compose -f $(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)

# Tear down everything
down:
	@echo "🧹 Shutting down and removing containers..."
	docker compose -f $(DOCKER_COMPOSE) down

# Remove build cache
clean:
	@echo "🧽 Removing Docker build cache..."
	docker builder prune -f

# Shortcut to restart job service only
restart-job:
	docker compose -f $(DOCKER_COMPOSE) stop $(SERVICE_NAME)
	docker compose -f $(DOCKER_COMPOSE) rm -f $(SERVICE_NAME)
	DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose -f $(DOCKER_COMPOSE) up --build $(SERVICE_NAME)

# One-liner: Build, create network, and run all services
pipeline:
	make clean && make rebuild && make up

