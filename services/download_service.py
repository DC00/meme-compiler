from yt_dlp import YoutubeDL

class DownloadService:
    
    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.ydl = YoutubeDL()
        return self
    
    def download(self, urls):
        # works for youtube and tiktok urls
        self.ydl.download(urls)
    

if __name__ == '__main__':
    ds = DownloadService.build()
    
    URLS = ['https://www.tiktok.com/@beis7/video/7121896431325056262']

    ds.download(URLS)