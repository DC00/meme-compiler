import glob
from yt_dlp import YoutubeDL
from google.cloud import storage


class VideoService:

    BUCKET_NAME = "videos-4a7a2084ee0b4369b5667ce2d01c530d"

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        params = {
            "restrictfilenames": True,
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
            "paths": {
                "home": "./"
            },
            "outtmpl": "%(title)s_%(extractor)s[%(id)s].%(ext)s"
        }
        self.ydl = YoutubeDL(params)
        self.storage = storage.Client()
        self.bucket = self.storage.bucket(self.BUCKET_NAME)

        return self

    def download(self, urls):
        self.ydl.download(urls)

        return glob.glob("*.mp4")

    def backup(self, urls):
        videos = self.download(urls)

        uploaded = [ v for v in videos if self.upload(v) ]

        print(f"Uploaded {len(uploaded)} videos to storage bucket")

    def upload(self, video):
        blob = self.bucket.blob(video)

        return False if blob.exists() else (not blob.upload_from_filename(f"./{video}"))

if __name__ == "__main__":
    vs = VideoService.build()

    URLS = ["https://www.youtube.com/watch?v=BaW_jenozKc"]

    vs.download(URLS)