# Meme Compiler

Generates a compilation video from submitted video urls

## Install

`pip install -r requirements.txt`

## Setup

### Google Auth Creds

https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python

- Go to google cloud console: console.cloud.google.com
- Go to `meme-compiler` project
- Select "Service Accounts" and click on the service account for the project
- Go to "Keys"
- Create or download a json file with provided service account keys
- Add to environment variable: `export GOOGLE_APPLICATION_CREDENTIALS='path/to/creds.json'`

