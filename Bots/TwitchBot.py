import irc.bot
import requests


# Extend IRC bot with Twitch specifics
class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username: str, client_id: str, token: str, channels:[str], port: int =6667) -> None:
        self.empty_list = []
        self.username = username
        self.client_id = client_id
        self.token = token
        self.channel_names = channels
        self.channel_urls = {channel: 'https://api.twitch.tv/kraken/users?login=' + channel for channel in channels}
        self.channel_ids = dict()

        # Get the channel id, we will need this for v5 API calls
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        for channel in self.channel_names:
            try:
                r = requests.get(self.channel_urls[channel], headers=headers).json()
                self.channel_ids[channel] = r['users'][0]['_id']
            except KeyError as e:
                print("Failed to get channel id for {}".format(channel))
                print(e)
                exit(0)

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        print("Connecting to {} on port {}...".format(server, port))
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, connection, event):
        print(self.channel_names)
        for channel in self.channel_names:
            print("Attempting to join {}".format(channel))
            # Generating token from https://twitchapps.com/tmi/ has default chat viewing privileges
            # Otherwise would need to request them when creating the OAuth token
            connection.join('#' + channel)

    def on_pubmsg(self, connection, event):
        # TODO:  Save message in database for use in WordCloud creation
        print("{} - {} :{}".format(event.target, event.source.split('!', 0)[0], event.arguments[0]))
        return
