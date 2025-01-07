# Include the .env file to load variables into the Makefile
include .env

VIDEO_PATH     = ./internal/video/
CONTAINER_NAME = mcc

setup:
	brew install liquibase

build:
	gofmt -s -w .
	cd $(VIDEO_PATH) && go build -v -o ../../mc main.go

run:
	PORT=$(PORT) DOWNLOAD_BUCKET=$(DOWNLOAD_BUCKET) ./mc

gen:
	./scripts/openapi-http.sh video internal/video/port port

clean:
	rm -f mc

docker:
	docker build --platform linux/amd64 -t mc .

docker.run:
	docker run --platform linux/amd64 -it --rm --name $(CONTAINER_NAME) -p $(PORT):$(PORT) --env-file .env mc

db.validate:
	cd sql && liquibase validate

db.update:
	cd sql && liquibase update
