from yt_dlp import YoutubeDL
from datetime import datetime

class Response:

    def __init__(self, timestamp, url, start_at, end_at):
        self.timestamp = timestamp
        self.url = url
        self.start_at = start_at
        self.end_at = end_at

    def is_valid(self):
        return self.valid_url() and self.valid_timestamps()

    def valid_url(self):
        return len(self.url) <= 255

    def valid_timestamps(self):
        if self.has_timestamps():
            start = self.to_seconds(self.start_at)
            end = self.to_seconds(self.end_at)

            return (start >= 0 and end > 0) and (start < end)

        return True

    def has_timestamps(self):
        return bool(self.start_at and self.end_at)

    def to_seconds(self, time):
        try:
            date = datetime.strptime(time, "%M:%S")

            minutes, seconds = date.minute, date.second

            return 60 * minutes + seconds
        except ValueError:
            return -1


    def params(self):

        # callback function executed from within yt-dlp https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L437
        def download_ranges(_info_dict, _ydl):
            return [{
                "start_time": self.to_seconds(self.start_at),
                "end_time": self.to_seconds(self.end_at)
            }]

        params = {
            "restrictfilenames": True,
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
            "paths": {
                "home": "./"
            },
            "outtmpl": "%(title)s_%(extractor)s[%(id)s].%(ext)s",
            "sleep_interval": 0.1
        }

        if self.has_timestamps():
            params = params | { "download_ranges": download_ranges }

        return params

    def download(self):
        downloader = YoutubeDL(self.params())

        return downloader.download(self.url)
