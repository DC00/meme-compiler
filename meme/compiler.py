import meme

class Compiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = meme.FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
        self.video_service = meme.VideoService.build()
        self.database_service = meme.DatabaseService.build()

        return self

