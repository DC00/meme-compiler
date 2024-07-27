# Concatenate

Combines normalized videos together for a final meme compilation. The Meme Compiler.

Currently using the cloud storage package to download/upload/remove videos from buckets because the gsutil sdk is not included in Cloud Functions. Cloud Functions are cheaper than Cloud Run invocations so went trying to use them as much as possible.

## FFmpeg
There are two approaches for concatenating videos with FFmpeg, copying and reencoding. Reencoding takes much longer because we are reprocessing every video. Copying will just try to attach each video to the end of another. I've seen some issues where the audio gets out of sync with copying, but normalizing each video beforehand should remediate most of the timestamping issues.

```
ffmpeg", "-f", "concat", "-safe", "0", "-i", videoListFile, "-c", "copy", outputFile
```

vs


```
ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", videoListFile,
    "-c:v", "libx264",
    "-preset", "veryslow",
    "-crf", "21",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-ar", "48000",
    "-b:a", "384k",
```