class Serializer:

    @classmethod
    def build(cls, obj):
        return cls(obj).serialize()

    def __init__(self, obj):
        self.obj = obj

    def serialize(self):
        match type(self.obj.__name__):
            case "Response":
                return self.build_response()
            case "Video":
                return self.build_video()
            case "Metadata":
                return self.build_metadata()

        return None

    def build_response(self):
        return {
            "id": self.id,
            "url": self.url,
            "video_id": self.video_id,
            "start_at": self.start_at,
            "end_at": self.end_at,
            "entered_at": self.entered_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def build_video(self):
        return {
            "id": self.id,
            "platform": self.platform,
            "identifier": self.identifier,
            "storage_link": self.storage_link,
            "format": self.format,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def build_metadata(self):
        return {
            "id": self.id,
            "response_id": self.response_id,
            "video_id": self.video_id,
            "url": self.url,
            "platform": self.platform,
            "identifier": self.identifier,
            "filename": self.filename,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
