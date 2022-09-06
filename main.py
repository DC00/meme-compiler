from meme import *
from yt_dlp import YoutubeDL


import pdb


fs = FormService.build("1oizPnNYIEzSLL6CrjlAMZdySw90jfTJf_2X9SFHejTM")
# vs = VideoService.build()
ds = DatabaseService.build()
# mc  = Compiler.build()

# extract info for each and add to metadata table
responses = ds.get_responses()

def get_metadata(response):
    metadata = response.metadata()

    downloader = YoutubeDL(params)

    info = downloader.extract_info(params["mc_url"], download=False)

    filename = downloader._prepare_filename(info)

    return Metadata.create(response, filename)

metadatas = [ get_metadata(response) for response in responses ]

metadatas = [ m for m in metadatas if m.is_valid() and not ds.metadata_exists(m) ]

print(f"adding {len(metadatas)} metadatas")

ds.add_metadata(metadatas)

print("done")





