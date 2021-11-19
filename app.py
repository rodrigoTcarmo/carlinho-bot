import os
import slack
from pathlib import Path
from slack_bolt import App
from flask import Flask
from library import Library
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
bot_id = client.api_call("auth.test")['user_id']


class Listen:
    def __init__(self):
        self.get = None
        pass

    @slack_event_adapter.on('message')
    def get_message(payload):
        event = payload.get('event', {})
        channel_id = event.get('channel')
        user_id = event.get('user')
        text_message = event.get('text')

        message_dict = {
            "event": event,
            "channel_id": channel_id,
            "user_id": user_id,
            "text_message": text_message
        }
        # if bot_id != user_id:
        #     client.chat_postMessage(channel=channel_id, text=text_message)
        A = Analytics(message_dict)
        A.analyze_message(use_split_message=A.treat_message())


class Analytics:
    def __init__(self, use_message_dict):
        self.split_message = use_message_dict["text_message"].split()

    def treat_message(self):
        return [w.upper() for w in self.split_message]

    def analyze_message(self, use_split_message):
        from library import Library
        L = Library()
        match_word = (set(L.dictionary()) & set(use_split_message))

        if match_word:
            match = [s for s in match_word if s][0]
            print('achei palavra:', match)
            Analytics.search_books(self, search_topic=match)

        else:
            print('não achei palavra')

    def search_books(self, search_topic):
        from library import Library

        print(search_topic)

        read_book = Library().bookshelf()
        print(read_book[search_topic])


if __name__ == "__main__":
    app.run(debug=True)
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
