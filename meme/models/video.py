import re

class Video:

    @classmethod
    def build(cls, path):
        return cls(path).create()

    def __init__(self, path):
        self.path = path

    def create(self):
        self.platform, self.identifier = self.format()

        return self

    def format(self):
        try:
            platform = re.search(r"(?i)(youtube|tiktok)", self.path)
            platform = platform.groups()[-1]
            platform = platform.lower()

            identifier = re.search(r"(?i)(\[)(.*)(\])", self.path)
            identifier = identifier.groups()[1]

            return (platform, identifier)

        except (AttributeError, IndexError):
            print("MEME_COMPILER::ERROR: Could not parse video platform and/or identifier")
            return None

    def key(self):
        return f"{self.platform}-{self.identifier}"
