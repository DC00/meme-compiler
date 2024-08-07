# MemeCompiler
An API to download, normalize, and create compilations of funny videos

## Setup
Steps needed to configure publishing to Google Artifact Registry. Guided link [here](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images).

- Create new registry
- `gcloud auth login`
- Configure gcloud: `gcloud auth configure-docker us-east4-docker.pkg.dev`

## Development

Build the container
```
docker build -t mc-api .
```
Tag the container
```
docker tag \
    <local-container-name> \
    <region>-docker.pkg.dev/<project-name>/<artifact-registry-name>/<image-name>:tag
```

Example:
```
docker tag \
    mc-api \
    us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mc-api:1.0.0
```

Push the image
```
docker push \
    us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mc-api:1.0.0
```

Pull the image
```
docker pull \
    us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mc-api:1.0.0
```

