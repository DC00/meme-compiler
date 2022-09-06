from meme import *
from yt_dlp import YoutubeDL

import pdb

fs = FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
# vs = VideoService.build()
ds = DatabaseService.build()
# mc  = Compiler.build()

responses = fs.read()
print("adding responses to db")
print(ds.add_responses(responses[0:10]))
