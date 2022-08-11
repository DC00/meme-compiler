import re

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
        regex = re.compile("\d{2}:\d{2}")

        if self.start_at or self.end_at:
            return regex.match(self.start_at) and regex.match(self.end_at)

        return True