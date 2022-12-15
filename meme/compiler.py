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
        responses = self.form_service.read()

        metadata = self.video_service.ingest(responses[0:limit])

        self.form_service.ingest(metadata)

    def store(self, limit=10):
        responses = self.form_service.read()

        self.video_service.store(responses[0:limit])

    def download(self, limit=10):
        responses = self.form_service.read()

        self.video_service.download(responses[0:limit])
