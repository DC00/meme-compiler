from meme import *


fs = FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
# vs = VideoService.build()
ds = DatabaseService.build()
# mc  = Compiler.build()

responses = fs.read()
print("adding responses to db")
ds.add_responses(responses)






