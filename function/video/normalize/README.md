# Normalize

**Cloud Function** which runs ffmpeg to normalize the size and audio of a video. Triggered by an Eventarc notification when a new object is written to the GCS bucket.
Cloud Functions are a lot cheaper than Cloud Run invocations but are limited to packages that are included in the runtime environment (FFmpeg [is included](https://cloud.google.com/functions/docs/reference/system-packages)).
You can also pull the base Go images [here](https://cloud.google.com/functions/docs/concepts/execution-environment).
```
docker pull \
    us-central1-docker.pkg.dev/serverless-runtimes/google-22-full/runtimes/go122:go122_20240609_1_22_3_RC00

docker run -u root -it --rm us-central1-docker.pkg.dev/serverless-runtimes/google-22-full/runtimes/go122:go122_20240609_1_22_3_RC00 /bin/bash
```

Not using a Dockerfile because we are uploading the code within main.go directly to Google Cloud Functions. The Cloud Functions Framework will wrap and execute the function.

#### Testing

View the testing instructions at Google Cloud Function Console -> select cloud function (mcf-normalize) -> Testing -> Curl command
