import meme
from meme.lib.adapters.metadata_adapter import MetadataAdapter

class Compiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = meme.FormService.build()
        self.video_service = meme.VideoService.build()
        # self.database_service = meme.DatabaseService.build()

        return self

    def ingest(self, limit=10):
        responses = self.form_service.read(limit)

        self.video_service.backup(responses)

    def download(self, limit=10):
        responses = self.form_service.read(limit)

        self.video_service.download(responses)




    # TODO: Implement after adding DB service
    # def ingest(self):
    #     adapter = MetadataAdapter()

    #     responses = self.form_service.read()

    #     metadata = [ response.metadata(adapter) for response in responses ]
    #     metadata = [ m for m in metadata if m.is_valid() ]

    #     return metadata

    #     # TODO:
    #     # create video row
    #     # create response row
    #     # create metadata row

    # def backup(self):
    #     # TODO:
    #     # for each video with storage_link = null
    #     #   download video to google storage
    #     #   populate storage_link on video row
    #     pass

    # def download(self, limit=10):
    #     # TODO:
    #     # download up to "limit" videos from google storage
    #     pass