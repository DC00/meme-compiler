class DatabaseService:

    PROJECT_ID = "meme-compiler"
    VIDEO_COLLECTION = u"videos"
    RESPONSE_COLLECTION = u"responses"

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.db = firestore.Client(project=self.PROJECT_ID)

    def add_video(self, video):
        reference = self.db.collection(self.VIDEO_COLLECTION).document(video.key())
