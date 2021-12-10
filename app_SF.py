from slack import RTMClient
import requests
import os
from dotenv import load_dotenv


@RTMClient.run_on(event="message")
def bot(**payload):
    print("BATEU AQUI")
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")

    if bot_id == "":
        channel_id = data["channel"]

        text = data.get("text", "")
        text = text.split(">")[-1].strip()

        response = ""
        if "help" in text.lower():
            user = data.get("user", "")
            response = f"Oi <@{user}>! EU sou O **** DO BOT RESPONDENDO"
        else:
            response = "Oi eu sou o bot formal"

        web_client.chat_postMessage(channel=channel_id, text=response)


if __name__ == "__main__":
    try:
        rtm_client = RTMClient(token="xoxb-2659335230855-2820319512709-U2JbFx6h86Bs8w0LJNQt2NNF")
        rtm_client.start()
        print("Bot is up and running!")

    except Exception as err:
        print(err)