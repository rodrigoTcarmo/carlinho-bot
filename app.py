import os
import slack
from pathlib import Path
from slack_bolt import App
from flask import Flask
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

class Message():
    def __init__(self):
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
        f = Message()
        f.analyze_message(use_split_message=f.treat_message(use_message_dict=message_dict))

    def treat_message(self, use_message_dict):
        split_message = use_message_dict["text_message"].split()
        return split_message

    def analyze_message(self, use_split_message):
        dict_words = ['jira', 'aws', 'jenkins']

        match = (set(dict_words) & set(use_split_message)).remove("{''}")

        if match:
            print('achei palavra:', match)
            Message().search_books(search_topic=match)

        else:
            print('não achei palavra')

    def search_books(self, search_topic):
        from book import Library

        print(search_topic)

        l = Library().bookshelf()
        print(l[search_topic])


"""class Data():
    def __init__(self):
        pass

    def start_somethig(self, data_dict):
        print(data_dict)"""

if __name__ == "__main__":
    app.run(debug=True)
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
