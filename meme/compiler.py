from meme.services import FormService
from meme.services import VideoService

class Compiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = FormService.build()
        self.video_service = VideoService.build(force=True)

        return self

    def ingest(self, limit=10):
        responses = self.form_service.read(limit)

        self.video_service.backup(responses)

    def download(self, limit=10):
        responses = self.form_service.read(limit)

        self.video_service.download(responses)
