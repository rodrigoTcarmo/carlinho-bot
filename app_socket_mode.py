import os
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient

load_dotenv()

# Initialize SocketModeClient with an app-level token + WebClient
"""client = SocketModeClient(

    # This app-level token will be used only for establishing a connection
    app_token=os.environ.get("SLACK_APP_TOKEN"),

    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
)"""

# from slack_sdk.socket_mode.response import SocketModeResponse
# from slack_sdk.socket_mode.request import SocketModeRequest

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)


@app.client.conversations_info(channel="C02L6J53E65")
def mention_handler():
    pass


"""def process(client: SocketModeClient, req: SocketModeRequest):
    me = client.web_client.conversations_info(channel="C02L6J53E65")
    print(me)

    if req.type == "events_api":
        print(req.type)
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)

        client.send_socket_mode_response(response)

        # Add a reaction to the message if it's a new message
        if req.payload["event"]["type"] == "message" and req.payload["event"].get("subtype") is None:
            client.web_client.reactions_add(name="eyes",
                                            channel=req.payload["event"]["channel"],
                                            timestamp=req.payload["event"]["ts"],
                                            )

            get_response = req.payload["event"]["text"].split()

            get_match_word = analyze_message(event_text=get_response, payload=req.payload)
            get_info = search_library(use_match=get_match_word)

            client.web_client.chat_postMessage(channel="#estudos",
                                               text=get_info)

    if req.type == "interactive" and req.payload.get("type") == "shortcut":
        if req.payload["callback_id"] == "hello-shortcut":
            print(req.type)
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

            # Open a welcome modal
            client.web_client.views_open(
                trigger_id=req.payload["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "hello_modal",
                    "title": {
                        "type": "plain_text",
                        "text": "Greetings!"
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Good Bye"
                    },
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hello!"
                            }
                        }
                    ]

                }
            )

    if req.type == "interactive" and req.payload.get("type") == "view_submission":
        if req.payload["view"]["callback_id"] == "hello-modal":
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)


def analyze_message(event_text, payload):
    try:
        from library import Library
        L = Library()

        dict = [d.upper() for d in L.dictionary()]
        message = [m.upper() for m in event_text]

        match_word = (set(dict) & set(message))
        if match_word:
            match = [s for s in match_word][0]
            print("Palavra encontrada: ", match)

            return match

    except Exception as e_a:
        print(e_a)


def search_library(use_match):
    from library import Library
    read_book = Library().bookshelf()

    return read_book[use_match]"""


if __name__ == "__main__":

    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
    # Add a new listener to receive messages from Slack
    # You can add more listeners like this
    # client.socket_mode_request_listeners.append(process)

    # Establish a WebSocket connection to the Socket Mode servers
    # client.connect()

    # Just not to stop this process
    # from threading import Event
    # Event().wait()

