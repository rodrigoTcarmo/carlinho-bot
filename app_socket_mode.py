import os
import slack
from pathlib import Path
from slack_bolt import App
from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt.workflows.step import WorkflowStep
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = App(token=os.environ["SLACK_BOT_TOKEN"])


def edit(ack, step, configure):
    ack()

    blocks = [
        {
            "type": "input",
            "block_id": "task_name_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "name",
                "placeholder": {"type": "plain_text", "text": "Add a task name"},
            },
            "label": {"type": "plain_text", "text": "Task name"},
        },
        {
            "type": "input",
            "block_id": "task_description_input",
            "element": {
                "type": "plain_text_input",
                "action_id": "description",
                "placeholder": {"type": "plain_text", "text": "Add a task description"},
            },
            "label": {"type": "plain_text", "text": "Task description"},
        },
    ]
    configure(blocks=blocks)


def save(ack, view, update):
    ack()

    values = view["state"]["values"]
    task_name = values["task_name_input"]["name"]
    task_description = values["task_description_input"]["description"]

    inputs = {
        "task_name": {"value": task_name["value"]},
        "task_description": {"value": task_description["value"]}
    }
    outputs = [
        {
            "type": "text",
            "name": "task_name",
            "label": "Task name",
        },
        {
            "type": "text",
            "name": "task_description",
            "label": "Task description",
        }
    ]
    update(inputs=inputs, outputs=outputs)

def execute(step, complete, fail):
    inputs = step["inputs"]
    # if everything was successful
    outputs = {
        "task_name": inputs["task_name"]["value"],
        "task_description": inputs["task_description"]["value"],
    }
    complete(outputs=outputs)

    # if something went wrong
    error = {"message": "Just testing step failure!"}
    fail(error=error)

# Create a new WorkflowStep instance
ws = WorkflowStep(
    callback_id="add_task",
    edit=edit,
    save=save,
    execute=execute,
)

# Pass Step to set up listeners
app.step(ws)

###############################################
@app.event("app_mention")
def mention_handler(body, ack):
    ack(f"Oi <@{body['user_id']}>!")


flask_app = Flask(__name__)

handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
