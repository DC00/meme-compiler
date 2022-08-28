import glob
import json
from google.cloud import storage
from adapter import Adapter


class VideoService:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.storage = storage.Client()

        with open("config.json", "r") as f:
            data = json.loads(f.read())
            self.bucket_name = data["bucket"]

        self.bucket = self.storage.bucket(self.bucket_name)
        self.adapter = Adapter(self.bucket)

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
