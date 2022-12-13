class Metadata:

    PLATFORMS = ["youtube", "tiktok"]

    def __init__(self, params):
        self.platform = params["platform"]
        self.identifier = params["identifier"]
        self.filename = params["filename"]

    def __repr__(self):
        return f"Metadata(platform={self.platform}, identifier={self.identifier}, filename={self.filename}"

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
