# Meme Compiler Cloud Functions

Contains cloud functions for downloading, normalizing, and concatenating video files.

Use Cloud Functions if everything you need is provided in a language's standard library.
Use Cloud Run if you need external dependencies installed outside of what is provided by Cloud Functions.

Cloud Run [contract](https://cloud.google.com/run/docs/container-contract) - use port 8080.
Dockerfiles should be multi-staged. I did not sys admin enough to create non-root users at the end of a Dockerfile stage, but should do that in the future.

## Admin Setup
Steps needed to configure publishing to Google Artifact Registry. Guided link [here](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images).

- Create new registry
- `gcloud auth login`
- Configure gcloud: `gcloud auth configure-docker us-east4-docker.pkg.dev`

## Development
Basic structure will follow the Google [tutorial](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-go-service).
More examples [here](https://github.com/GoogleCloudPlatform/golang-samples/tree/main/run).

Sample function structure:
```
my-package/
    Dockerfile
    go.mod
    main.go
```

Build the container
```
docker build -t mcf-download .
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
    mcf-download \
    us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mcf-download:1.0.0
```

Push the image
```
docker push \
    us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mcf-download:1.0.0
```

Pull the image
```
docker pull \
    us-east4-docker.pkg.dev/meme-compiler/mc-artifacts/mcf-download:1.0.0
```

