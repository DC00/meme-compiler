class Metadata:

    PLATFORMS = ["youtube", "tiktok"]

    @classmethod
    def create(cls, params):
        return cls(params)

    def __init__(self, params):
        self.id          = params.get("id")
        self.response_id = params.get("response_id")
        self.video_id    = params.get("video_id")
        self.url         = params.get("url")
        self.platform    = params.get("platform")
        self.identifier  = params.get("identifier")
        self.filename    = params.get("filename")
        self.created_at  = params.get("created_at")
        self.updated_at  = params.get("updated_at")

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
