# Download

**Cloud Run** container which downloads a video using yt-dlp and uploads to a Google Cloud Storage bucket.

Cloud Run containers allow you to add external dependencies in a Dockerfile. I needed to add `yt-dlp` which does not come custom in the included [system packages](https://cloud.google.com/functions/docs/reference/system-packages).

## YT-DLP Command
`format=bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]`: Enforce mp4 video and m4a audio, or best available mp4

`outputTemplate=%(extractor)s-%(id)s.%(ext)s`: platform-identifier.filetype, e.g. youtube-BaWjenozKc.mp4

The output directory can be appended to the outputTemplate. So `-o /tmp/youtube-BaWjenozKc.mp4` will store the video in the `/tmp` directory.

## Cloud Storage
Google Cloud Run can access the storage buckets through Background context:
```
ctx := context.Background()
client, err := storage.NewClient(ctx)
```

## Background Processing
The Cloud Run container will exit as soon as the HTTP request returns. This means goroutines and background processing will not work because the HTTP request finishes too early. Google has an option to keep the [CPU always on](https://cloud.google.com/run/docs/configuring/cpu-allocation) which makes backgrounding possible - however the price will increase. The breakeven point for always-on pricing vs request-only pricing with 1 CPU is about 0.7 requests/second (from Claude.ai after feeding in the Tier 1 pricing tables [here](https://cloud.google.com/run/pricing)).

## Docker

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
