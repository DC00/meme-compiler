import re

class Video:

    @classmethod
    def create(cls, path):
        return cls(path).build()

    def __init__(self, path):
        self.path = path

    def is_valid(self):
        return self.__valid_path()

    def build(self):
        self.platform, self.identifier = self.format()

        return self

    def format(self):
        try:
            platform = re.findall(r"(?i)(youtube|tiktok)", self.path)
            platform = platform[-1]
            platform = platform.lower()

            identifier = re.findall(r"(?i)\[(.*)\]", self.path)
            identifier = identifier[-1]

            return (platform, identifier)

        except (AttributeError, IndexError, TypeError):
            print("MEME_COMPILER::ERROR: Could not parse video platform and/or identifier")
            return None

    def key(self):
        return f"{self.platform}-{self.identifier}"

    def __valid_path(self):
        return len(self.path) > 0
