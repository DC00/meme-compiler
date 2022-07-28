from yt_dlp import YoutubeDL

class DownloadService:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        params = {
            # Can append / bv*+ba/b but then will not enforce mp4
            # 'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        }
        self.ydl = YoutubeDL(params)
        return self

    def download(self, urls):
        # works for youtube and tiktok urls
        self.ydl.download(urls)


if __name__ == "__main__":
    ds = DownloadService.build()

    URLS = ["https://www.youtube.com/watch?v=BaW_jenozKc"]

    ds.download(URLS)