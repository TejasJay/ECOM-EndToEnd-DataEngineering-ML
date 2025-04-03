# Makefile to build, run, and push the data_sources microservice

-include .env.secrets


IMAGE_NAME=ecom_data_sources
TAG=latest
DOCKERHUB_USERNAME=tejasjay03

.PHONY: help build run push login test

help:
	@echo "Targets:"
	@echo "  build        - Build Docker image"
	@echo "  run          - Run the container locally"
	@echo "  login        - Docker login to DockerHub"
	@echo "  push         - Push to DockerHub"
	@echo "  test         - Run simulation locally with Python"

login:
	docker login -u $(DOCKERHUB_USERNAME) -p $(DOCKERHUB_PASSWORD)

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run --rm -it $(IMAGE_NAME):$(TAG)

push: build
	docker tag $(IMAGE_NAME):$(TAG) $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG)
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE_NAME):$(TAG)

test:
	python3 -m pos_logs.unified_simulator --mode batch --count 10

batch:
	docker run --rm -it ecom_data_sources:latest python3 -m pos_logs.unified_simulator --mode batch --count 1000 --avg_sessions 10

realtime:
	docker run --rm -it ecom_data_sources:latest python3 -m pos_logs.unified_simulator --mode realtime --output kafka --avg_sessions 10 --concurrent_users 500


check-secrets:
	@if [ ! -f .env.secrets ]; then \
		echo "❌ .env.secrets file not found!"; \
		exit 1; \
	else \
		echo "✅ secrets loaded from .env.secrets "; \
	fi
