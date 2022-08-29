class Compiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
        self.video_service = VideoService.build()

        return self

    def ingest(self):
        responses = self.form_service.responses
        self.video_service.download(responses)

    def backup(self):
        responses = self.form_service.responses
        self.video_service.backup(responses)

if __name__ == "__main__":
    compiler = MemeCompiler.build()

    compiler.backup()

    # TODO: combine videos with ffmpeg
