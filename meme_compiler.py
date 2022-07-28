from services import *

class MemeCompiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
        self.download_service = DownloadService.build()
        return self

    def ingest(self):
        urls = self.form_service.urls()
        self.download_service.download(urls)

if __name__ == "__main__":
    compiler = MemeCompiler.build()

    compiler.ingest()

    # TODO: combine videos with ffmpeg
