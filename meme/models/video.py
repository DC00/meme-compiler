class Video:

    PLATFORMS = ["youtube", "tiktok"]

    def __init__(self, platform, identifier, storage_link):
        self.platform = platform
        self.identifier = identifier
        self.storage_link = storage_link

    def __repr__(self):
        return f"Video(platform={self.platform}, identifier={self.identifier}, storage_link={self.storage_link}"

    def is_valid(self):
        return self.__valid_platform() and self.__valid_identifier()

    def key(self):
        return f"{self.platform}-{self.identifier}"

    def __valid_platform(self):
        if self.platform in self.PLATFORMS:
            return True

        return False

    def __valid_identifier(self):
        return len(self.identifier) > 0
