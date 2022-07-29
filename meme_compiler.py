from services import *

class MemeCompiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
        self.video_service = VideoService.build()

        return self

    def ingest(self):
        urls = self.form_service.urls()
        self.video_service.download(urls)

    def backup(self):
        urls = self.form_service.urls()
        self.video_service.backup(urls)

if __name__ == "__main__":
    compiler = MemeCompiler.build()

    compiler.backup()

    # TODO: combine videos with ffmpeg
