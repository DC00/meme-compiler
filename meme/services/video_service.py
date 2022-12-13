import json
import glob

from google.cloud import storage

import meme

class VideoService:

    @classmethod
    def build(cls, **params):
        return cls(params).setup()

    def __init__(self, params):
        self.force = params["force"]

    def setup(self):
        self.storage = storage.Client()

        with open("config.json", "r") as f:
            data = json.loads(f.read())
            self.bucket_name = data["bucket"]

        self.bucket = self.storage.bucket(self.bucket_name)
        self.adapter = meme.VideoAdapter(self.bucket, self.force)

        return self

    def download(self, responses):
        [ response.download(self.adapter) for response in responses ]

        return glob.glob("*.mp4")

    def backup(self, responses):
        videos = self.download(responses)

        uploaded = [ v for v in videos if self.upload(v) ]

        print(f"Uploaded {len(uploaded)} videos to storage bucket")

    def upload(self, video):
        blob = self.bucket.blob(video)

        return False if blob.exists() else (not blob.upload_from_filename(f"./{video}"))
