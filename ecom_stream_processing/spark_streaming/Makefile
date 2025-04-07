# Makefile for building and running Spark Streaming job from spark_streaming/

IMAGE_NAME=spark_streaming
DOCKERFILE=Dockerfile
NETWORK_NAME=kafka_net

# Build the Docker image (context is current directory)
build:
	docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

# Run the container and execute Spark job
run:
	docker run --rm --network $(NETWORK_NAME) $(IMAGE_NAME)

# Rebuild and run the container
rebuild-run: build run
