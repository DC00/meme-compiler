from yt_dlp import YoutubeDL
from urllib.error import HTTPError

# used for downloading each video
class VideoAdapter:

    def __init__(self, bucket):
        self.bucket = bucket

    def download(self, params):
        downloader = YoutubeDL(params)

        try:
            info = downloader.extract_info(params["mc_url"], download=False)
        except:
            print(f"MEME_COMPILER:INFO: Error when downloading video")
            return

        filename = downloader._prepare_filename(info)

        blob = self.bucket.blob(filename)

        if blob.exists():
            print(f"MEME_COMPILER:INFO:{filename} already in google cloud")

        return [ downloader.download(params["mc_url"]) if not blob.exists() else None ]
