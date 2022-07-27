from services import *

class MemeCompiler:

    @classmethod
    def build(cls):
        return cls().setup()

    def setup(self):
        self.form_service = FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
        return self

if __name__ == '__main__':
    compiler = MemeCompiler.build()
    print(compiler.form_service.urls())
