# Makefile to build, run, and push the data_sources microservice

IMAGE_NAME=ecom_data_sources
TAG=latest
DOCKERHUB_USERNAME=your_dockerhub_username

.PHONY: help build run push login test

help:
	@echo "Targets:"
	@echo "  build        - Build Docker image"
	@echo "  run          - Run the container locally"
	@echo "  login        - Docker login to DockerHub"
	@echo "  push         - Push to DockerHub"
	@echo "  test         - Run simulation locally with Python"

login:
	docker login -u $(DOCKERHUB_USERNAME)

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run --rm -it $(IMAGE_NAME):$(TAG)

push: build
	docker tag $(IMAGE_NAME):$(TAG) $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG)
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG)

test:
	python3 -m pos_logs.unified_simulator --mode batch --count 10


