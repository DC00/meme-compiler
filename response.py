from datetime import datetime

class Response:

    MAX_DURATION_SECONDS = 180

    def __init__(self, timestamp, url, start_at, end_at):
        self.timestamp = timestamp
        self.url = url
        self.start_at = start_at
        self.end_at = end_at

    def is_valid(self):
        return self.__valid_url() and self.__valid_timestamps()

    def params(self):

        # https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L437
        def download_ranges(*_):
            return [{ "start_time": self.__to_seconds(self.start_at), "end_time": self.__to_seconds(self.end_at) }]

        # https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L402
        def max_duration(info, *, incomplete):
            duration = info.get("duration")

            if self.__has_timestamps():
                if self.__duration() > self.MAX_DURATION_SECONDS:
                    return f"Error: video is longer than {self.MAX_DURATION_SECONDS} seconds"
                return None

            if duration and duration > self.MAX_DURATION_SECONDS:
                return f"Error: video is longer than {self.MAX_DURATION_SECONDS} seconds"

        params = {
            "mc_url": self.url,
            "restrictfilenames": True,
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
            "paths": {
                "home": "./"
            },
            "outtmpl": "%(title)s_%(extractor)s[%(id)s].%(ext)s",
            "sleep_interval": 0.1,
            "match_filter": max_duration
        }

        if self.__has_timestamps():
            params = params | { "download_ranges": download_ranges }

        return params

    def download(self, adapter):
        return adapter.download(self.params())

    def __valid_url(self):
        return len(self.url) <= 255

    def __valid_timestamps(self):
        if self.__has_timestamps():
            start = self.__to_seconds(self.start_at)
            end = self.__to_seconds(self.end_at)

            return (start >= 0 and end > 0) and (start < end)

        return True

    def __has_timestamps(self):
        return bool(self.start_at and self.end_at)

    def __to_seconds(self, time):
        try:
            date = datetime.strptime(time, "%M:%S")

            minutes, seconds = date.minute, date.second

            return 60 * minutes + seconds
        except ValueError:
            return -1

    def __duration(self):
        return self.__to_seconds(self.end_at) - self.__to_seconds(self.start_at)
