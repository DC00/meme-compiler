from yt_dlp import YoutubeDL
from meme import Metadata

# Used for getting the metadata of each video
# will not download the video itself
class MetadataAdapter:

    def download(self, params):
        downloader = YoutubeDL(params)

        info = downloader.extract_info(params["mc_url"], download=False)

        url         = params["mc_url"]
        platform    = info["extractor"].lower()
        identifier  = info["id"]
        filename    = downloader._prepare_filename(info)

        params = {
            "url": url,
            "platform": platform,
            "identifier": identifier,
            "filename": filename
        }

        return Metadata(params)
