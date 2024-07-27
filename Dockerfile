FROM golang:1.22.4-bookworm AS build

ARG SERVICE=video

# Create and change to the internal service directory
WORKDIR /internal/$SERVICE

# Root user to install dependencies and build code
USER root

# Copy code to the container
COPY internal /internal/

# Build the service application
RUN go build -v -o /app .

# Use the official Debian slim image for a lean production container
FROM debian:bookworm-slim AS final

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends ca-certificates=20230311 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the binary to production image from build stage
COPY --from=build /app /app

CMD ["/app"]
