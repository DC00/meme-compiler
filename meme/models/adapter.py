from yt_dlp import YoutubeDL

class Adapter:

    def __init__(self, bucket):
        self.bucket = bucket

    def download(self, params):
        downloader = YoutubeDL(params)

        info = downloader.extract_info(params["mc_url"], download=False)

        filename = downloader._prepare_filename(info)

        blob = self.bucket.blob(filename)

        if blob.exists():
            print(f"MEME_COMPILER:INFO:{filename} already in google cloud")

        return [ downloader.download(params["mc_url"]) if not blob.exists() else None ]
