# spark_streaming/Makefile

IMAGE_NAME=spark_streaming
DOCKERFILE=Dockerfile
NETWORK_NAME=kafka_net

# Build Docker image with explicit architecture for Mac M1 or Linux
build:
	DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build \
		--tag $(IMAGE_NAME) \
		--file $(DOCKERFILE) .

# Run container in correct Kafka network
run:
	docker run --rm --network $(NETWORK_NAME) $(IMAGE_NAME)

# Shortcut for clean rebuild and run
rebuild-run: build run
