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

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text_message = event.get('text')

    if bot_id != user_id:
        client.chat_postMessage(channel=channel_id, text=text_message)

# Initializes your app with your bot token and socket mode handler
# app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Start your app
if __name__ == "__main__":
    app.run(debug=True)
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
