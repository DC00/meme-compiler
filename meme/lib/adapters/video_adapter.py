from yt_dlp import YoutubeDL
from urllib.error import HTTPError

# used for downloading each video
class VideoAdapter:

    def __init__(self, bucket, force):
        self.bucket = bucket
        self.force = force

    def download(self, params):
        downloader = YoutubeDL(params)

        try:
            info = downloader.extract_info(params["mc_url"], download=False)
        except:
            print(f"MEME_COMPILER:INFO: Error when downloading video")
            return

        filename = downloader._prepare_filename(info)

        blob = self.bucket.blob(filename)

        if not self.force and blob.exists():
            print(f"MEME_COMPILER:INFO:{filename} already in google cloud")

        return [ downloader.download(params["mc_url"]) if self.force or not blob.exists() else None ]
