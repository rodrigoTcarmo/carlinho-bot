import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient

# Initialize SocketModeClient with an app-level token + WebClient
client = SocketModeClient(

    # This app-level token will be used only for establishing a connection
    app_token=os.environ.get("SLACK_APP_TOKEN"),

    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest


def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        print(req.payload)
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)

        client.send_socket_mode_response(response)

        # Add a reaction to the message if it's a new message
        if req.payload["event"]["type"] == "message" and req.payload["event"].get("subtype") is None:
            client.web_client.reactions_add(name="eyes",
                                            channel=req.payload["event"]["channel"],
                                            timestamp=req.payload["event"]["ts"],
                                            )

        get_message = req.payload["event"]["text"]
        print(get_message)

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

# Add a new listener to receive messages from Slack
# You can add more listeners like this
client.socket_mode_request_listeners.append(process)

# Establish a WebSocket connection to the Socket Mode servers
client.connect()

# Just not to stop this process
from threading import Event
Event().wait()
