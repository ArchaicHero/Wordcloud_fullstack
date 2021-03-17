import irc.bot
import requests


# Extend IRC bot with Twitch specifics
class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username: str, client_id: str, token: str, channel:str, port: int =6667) -> None:
        self.username = username
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        print("Connecting to {} on port {}...".format(server, port))
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, c, e):
        print("Joining {}".format(self.channel))

        # Generating token from https://twitchapps.com/tmi/ has default chat viewing privileges
        # Otherwise would need to request them when creating the OAuth token
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        # TODO:  Save message in database for use in WordCloud creation
        print("Received chat message: '{}'".format(e.arguments[0]))
        return
