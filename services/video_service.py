from yt_dlp import YoutubeDL

class VideoService:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        # setup yt-dlp from yt-dlp.conf
        self.ydl = YoutubeDL()
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