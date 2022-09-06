import meme
from meme.lib.adapters.metadata_adapter import MetadataAdapter

class Compiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = meme.FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
        self.video_service = meme.VideoService.build()
        self.database_service = meme.DatabaseService.build()

        return self

    def ingest(self):
        adapter = MetadataAdapter()

        responses = self.form_service.read()

        metadata = [ response.metadata(adapter) for response in responses ]
        metadata = [ m for m in metadata if m.is_valid() ]

        # create video row
        # create response row
        # create metadata row

    def backup(self):
        # for each video with storage_link = null
        #   download video to google storage
        #   populate storage_link on video row
        pass

    def download(self, limit=10):
        # download up to "limit" videos from google storage
        pass
