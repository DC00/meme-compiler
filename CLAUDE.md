# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MemeCompiler is a Go-based API service for downloading, normalizing, and creating compilations of funny videos. The project uses a clean architecture pattern with distinct layers (domain, application, port, adapter) and leverages Google Cloud Platform services (Cloud Storage, Cloud Functions).

## Architecture

### Clean Architecture Layers
- **Domain Layer** (`internal/video/domain/`): Core business entities and repository interfaces
- **Application Layer** (`internal/video/app/`): Use cases organized as Commands (write operations) and Queries (read operations) following CQRS pattern
- **Port Layer** (`internal/video/port/`): HTTP handlers and OpenAPI-generated server code
- **Adapter Layer** (`internal/video/adapter/`): Infrastructure implementations (GCS repository)
- **Service Layer** (`internal/video/service/`): Application wiring and dependency injection

### Module Structure
The project uses multiple Go modules:
- `internal/video/`: Main API service module
- `internal/common/`: Shared utilities and clients
- `function/video/download/`: Cloud Function for video downloading
- `function/video/normalize/`: Cloud Function for video normalization
- `function/video/concatenate/`: Cloud Function for video concatenation
- `function/discord/`: Discord bot integration
- `function/example/`: Example function template

## Development Commands

### Build and Run
```bash
# Build the main API service
make build

# Run locally (requires .env file)
make run

# Build Docker container
make docker

# Run in Docker
make docker.run
```

### Code Generation
```bash
# Generate OpenAPI server and client code
make gen
# Or directly:
./scripts/openapi-http.sh video internal/video/port port
```

### Database Management (if Liquibase is configured)
```bash
# Validate database schema
make db.validate

# Apply database migrations
make db.update
```

### Setup
```bash
# Install required tools (Liquibase via Homebrew on macOS)
make setup
```

## API Development

The API is OpenAPI-first, defined in `api/openapi/video.yml`. Code generation creates:
- Server interfaces in `internal/video/port/openapi_*.gen.go`
- Client code in `internal/common/client/video/openapi_*.gen.go`

When modifying the API:
1. Edit `api/openapi/video.yml`
2. Run `make gen` to regenerate code
3. Implement any new handler methods in `internal/video/port/http.go`

## Environment Configuration

Required environment variables (see `.env.skel`):
- `PORT`: API server port
- `DOWNLOAD_FUNCTION_URL`: URL of the download Cloud Function
- `DOWNLOAD_BUCKET`: GCS bucket for downloaded videos
- `SERVICE_ACCOUNT`: GCP service account for authentication

## Docker Deployment

The project uses Google Artifact Registry for container storage:
```bash
# Build for linux/amd64
docker build --platform linux/amd64 -t mc-api .

# Tag for Artifact Registry
docker tag mc-api us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mc-api:1.0.0

# Push to registry
docker push us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mc-api:1.0.0
```