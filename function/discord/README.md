# Discord Bot

This is a Discord bot running as a Google Cloud Function which interacts with the [Meme Compiler API](https://github.com/DC00/meme-compiler). Current functionality implements the basic commands:

```
/ping: Pong
/addvideo [url]: Add a video to the meme compiler
/createcompilation: Creates a meme compilation
```

## Setup

The bot sends messages to an Interaction Endpoint URL which is triggered from the registered slash commands. We have to respond to PING requests as well as per the [documentation](https://discord.com/developers/docs/interactions/overview#setting-up-an-endpoint-acknowledging-ping-requests).

We decrypt Discord's requests with the Discord Public Key and send authenticated requests to the [Meme Compiler API](https://github.com/DC00/meme-compiler) with the gcloud Identity Token.

**Important Note:** The gcloud Identity Token will change sometimes. I need to investigate when this happens, but if the token does change we need to redeploy the Discord cloud function.

## Permissions

- Manage Webhooks
- Read messages/View Channels
- Send Messages
- Send Messages in Threads
- Add Reactions
- Use Slash Commands

Integer representing these permissions: `277562264640`. To recalculate, go to https://discord.com/developers/applications/ -> Select Bot -> Bot and select permissions again.

The OAuth invite link will be `https://discord.com/oauth2/authorize?client_id=<client_id>&scope=bot&permissions=277562264640`
