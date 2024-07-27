#!/bin/bash
# Requires an OpenAPI specification at api/openapi/<domain>.yml
# ./scripts/openapi-http.sh <domain> </path/to/output/directory> <package of port>
#
# Example:
# ./scripts/openapi-http.sh video internal/video/port port
set -e

# service = name of domain (video) and filename of the openapi file (video.yml)
# output_dir = output directory for the http server (chi) and types
# package = name of package (also video)
readonly service="$1"
readonly output_dir="$2"
readonly package="$3"

oapi-codegen -generate types -o "$output_dir/openapi_types.gen.go" -package "$package" "api/openapi/$service.yml"
oapi-codegen -generate chi-server -o "$output_dir/openapi_api.gen.go" -package "$package" "api/openapi/$service.yml"
oapi-codegen -generate types -o "internal/common/client/$service/openapi_types.gen.go" -package "$service" "api/openapi/$service.yml"
oapi-codegen -generate client -o "internal/common/client/$service/openapi_client.gen.go" -package "$service" "api/openapi/$service.yml"
