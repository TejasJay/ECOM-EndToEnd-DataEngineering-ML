IMAGE_NAME=spark_streaming
DOCKERFILE=Dockerfile
NETWORK_NAME=kafka_kafka_net

# Build Docker image with explicit architecture for Mac M1 or Linux
build:
	DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build \
		--tag $(IMAGE_NAME) \
		--file $(DOCKERFILE) .

# Create Docker network if it doesn't exist
network:
	docker network inspect $(NETWORK_NAME) >/dev/null 2>&1 || docker network create $(NETWORK_NAME)

# Run container in correct Kafka network
run: network
	docker run --rm --network $(NETWORK_NAME) $(IMAGE_NAME)

# Shortcut for clean rebuild and run
rebuild-run: build run
