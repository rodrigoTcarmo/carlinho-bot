import os
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
SIGNING_SECRET = os.environ.get("SIGNING_SECRET")

app = App(token=SLACK_BOT_TOKEN)


class Listen:
    def __init__(self):
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()

    @app.event("message")
    def get_data(message, say):
        raw_data = message

        user_id = raw_data['user']
        channel = raw_data['channel']
        text = raw_data['text']

        data = {
            "user_id": user_id,
            "channel": channel,
            "text": text
        }
        A = Analytics(use_data=data)
        A.analyze_message(use_split_message=A.sanitize())


class Analytics:
    def __init__(self, use_data):
        self.split_message = use_data['text'].split()
        self.user_id = use_data['user_id']
        self.text = use_data['text']

    def sanitize(self):
        return [w.upper() for w in self.split_message]

    def analyze_message(self, use_split_message):
        from library import Library
        L = Library()
        match_word = (set(L.dictionary()) & set(use_split_message))

        if match_word:
            match = [s for s in match_word if s][0]
            print('Achei palavra:', match)
            Lib(use_match=match).search_books()

        else:
            print("Não achei nada")


class Lib:
    def __init__(self, use_match):
        self.match = use_match

    def search_books(self):
        from library import Library
        print(self.match)

        read_book = Library().bookshelf()
        print(read_book[self.match])


if __name__ == "__main__":
    Listen()
