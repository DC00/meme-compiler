# Meme Compiler

Generates a compilation video from submitted video urls

## Setup

### Google Auth Creds

https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python

- Go to google cloud console: `console.cloud.google.com`
- Go to `meme-compiler` project
- Select "Service Accounts" and click on the service account for the project
- Go to "Keys"
- Create or download a json file with provided service account keys
- Add to environment variable:
```
export GOOGLE_APPLICATION_CREDENTIALS='path/to/creds.json'
```

### Environment

Create virtual environment:
```
virtualenv env
```

Source environment:
```
source env/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

### YT-DLP

Can optionally use the conf file as a command line argument for the executable:

```
yt-dlp --config-location ./yt-dlp.conf <url>
```

The configurations in the yt-dlp.conf file are also used in the python client YoutubeDL initialization. YT-DLP source code is hard to follow so  documenting what the parameters do here:

```
params = {
	"restrictfilenames": True,
	"format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
	"paths": {
		"home": "./"
	},
	"outtmpl": "%(title)s_%(extractor)s[%(id)s].%(ext)s"
}
```

`restrictfilenames`: Strip spaces and non-ASCII characters in filename

`format`: Best mp4 video with best m4a audio, or best available mp4

`paths`: Location of output directory

`outtmpl`: output filename format `video_title_without_spaces_youtube[video_id].mp4`

`ext`: file extension
