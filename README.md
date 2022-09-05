# Meme Compiler

Generates a compilation video from submitted video urls

## Setup

### Google Auth Creds

https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python

- Go to google cloud console: https://console.cloud.google.com
- Go to `meme-compiler` project
- Select "Service Accounts" and click on the service account for the project
- Go to "Keys"
- Create or download a json file with provided service account keys
- Add to environment variable:
```
export GOOGLE_APPLICATION_CREDENTIALS='path/to/creds.json'
```

### "Service Discovery"

Copy `config.json.skel` to `config.json`. Populate the Google Cloud bucket id and Heroku Postgres uri connection string

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

Validate python version
```
python -V
> Python 3.9.13
```

## Database

Heroku Hobby-dev PostgreSQL (need to upgrade by [November 28, 2022](https://help.heroku.com/RSBRUH58/removal-of-heroku-free-product-plans-faq))

Using [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html) for db versioning

### Apply database migrations
```
alembic upgrade head
```

### Revert database migrations
```
alembic downgrade -1
```


## Usage

#### Download videos into current directory

```
compiler = MemeCompiler.build()
compiler.ingest()
```

#### Backup videos to Google Storage
```
compiler = MemeCompiler.build()
compiler.backup()
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
	"outtmpl": "%(title)s_%(extractor)s[%(id)s].%(ext)s",
	"sleep_interval": 0.1,
	"match_filter": max_duration,
	"download_ranges": download_ranges
}
```

**field**|**description**
:-----:|:-----:
`restrictfilenames`| Strip spaces and non-ASCII characters in filename
`format`| Best mp4 video with best m4a audio
`paths`| Location of output directory
`outtmpl`| output filename format `video_title_without_spaces_youtube[video_id].mp4`
`sleep_interval`| I don't know if we need this
`match_filter` | duration check function called for each downloaded video
`download_ranges` | callback function which specifies time range to download
`ext`| file extension
