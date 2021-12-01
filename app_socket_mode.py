import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient

client = SocketModeClient(
    app_token=os.environ.get("SLACK_APP_TOKEN"),
    web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest


def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        if req.payload["event"]["type"] == "message" and req.payload["event"].get("subtype") is None:
            client.web_client.reactions_add(name="eyes",
                                            channel=req.payload["event"]["channel"],
                                            timestamp=req.payload["event"]["ts"],
                                            )

    if req.type == "interactive" and req.payload.get("type") == "shortcut":
        if req.payload["callback_id"] == "hello-shortcut":
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

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

client.socket_mode_request_listeners.append(process)

client.connect()

from threading import Event
Event().wait()
