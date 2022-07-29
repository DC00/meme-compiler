from yt_dlp import YoutubeDL

class VideoService:

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
        return self

    def download(self, urls):
        # works for youtube and tiktok urls
        self.ydl.download(urls)

    def backup(self, data):
        pass




if __name__ == "__main__":
    vs = VideoService.build()

    URLS = ["https://www.youtube.com/watch?v=BaW_jenozKc"]

    vs.download(URLS)