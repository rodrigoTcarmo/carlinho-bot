import os
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
SIGNING_SECRET = os.environ.get("SIGNING_SECRET")

app = App(token=SLACK_BOT_TOKEN)


@app.event("message")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
