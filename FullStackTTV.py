from Bots.TwitchBot import TwitchBot


def get_strings_from_file(filename: str) -> (str, str, [str]):
    # pull token from file not included in repo for now.  TODO: Move to OAuth2 on website so user can auth themselves
    with open(filename, 'r') as f:
        username = f.readline().rstrip().lower()
        client_id = f.readline().rstrip()
        auth = f.readline().rstrip()
        channels = [line.rstrip().lower() for line in f.readlines()]

    return username, client_id, auth, channels


if __name__ == '__main__':
    FILENAME = "TwitchStrings.txt"
    username, client_id, auth, channels = get_strings_from_file(FILENAME)

    bot = TwitchBot(username, client_id, auth, channels)
    bot.start()
