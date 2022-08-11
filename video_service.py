import glob
from google.cloud import storage


class VideoService:

    BUCKET_NAME = "videos-4a7a2084ee0b4369b5667ce2d01c530d"

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.storage = storage.Client()
        self.bucket = self.storage.bucket(self.BUCKET_NAME)

        return self

    def download(self, responses):
        [ response.download() for response in responses ]

        return glob.glob("*.mp4")

    def backup(self, responses):
        videos = self.download(responses)

        uploaded = [ v for v in videos if self.upload(v) ]

        print(f"Uploaded {len(uploaded)} videos to storage bucket")

    def upload(self, video):
        blob = self.bucket.blob(video)

        return False if blob.exists() else (not blob.upload_from_filename(f"./{video}"))
