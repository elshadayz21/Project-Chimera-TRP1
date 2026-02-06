IMAGE_NAME := chimera:dev

.PHONY: setup build test shell clean

build:
	docker build -t $(IMAGE_NAME) .

setup: build
	@echo "Setup complete: Docker image '$(IMAGE_NAME)' built with project dependencies."

test:
	@echo "Running tests inside Docker"
	docker run --rm -v $(PWD):/app -w /app $(IMAGE_NAME) pytest -q

spec-check:
	@echo "Running lightweight spec checks"
	python3 scripts/spec_check.py

shell:
	@echo "Starting shell inside Docker (interactive)"
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE_NAME) /bin/bash

clean:
	@echo "Removing image $(IMAGE_NAME)"
	docker rmi -f $(IMAGE_NAME) || true
