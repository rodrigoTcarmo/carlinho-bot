import os
from art import *
from slack_bolt import App
from dotenv import load_dotenv
from Logs.log_engine import LogEngine
from slack_bolt.adapter.socket_mode import SocketModeHandler
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)


class StartEngine:
    def __init__(self):
        """========== START BOT BANNER =========="""
        tprint("SAN FIERRO", "broadway")

        """========== START BOT ENGINE =========="""
        Listen()


class Listen:
    def __init__(self):
        self.data = None
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()

    @app.event("message")
    def get_data(message, say):
        raw_data = message

        user_id = raw_data['user']
        channel = raw_data['channel']
        text = raw_data['text']
        ts = raw_data['ts']

        data = {
            "user_id": user_id,
            "channel": channel,
            "text": text,
            "ts": ts
        }

        A = Analytics()
        A.get_data(use_data=data)

        A.analyze_message(use_split_message=A.sanitize())
        A.delivery_thread()


class Analytics:
    def __init__(self):
        self.split_message = None
        self.user_id = None
        self.channel = None
        self.text = None
        self.match = None
        self.ts = None

    def get_data(self, use_data):
        log.info("[!] - Collecting data")

        try:
            log.info("[!] - Getting split text message...")
            self.split_message = use_data['text'].split()
            log.info("[:P] - Success!\n")

        except Exception as split_text_err:
            log.info("[X] - Error getting text message!")
            log.info(split_text_err)

        try:
            log.info("[!] - Getting user ID...")
            self.user_id = use_data['user_id']
            log.info("[:P] - Success!\n")

        except Exception as userid_err:
            log.info("[X] - Error getting user ID!")
            log.info(userid_err)

        try:
            log.info("[!] - Getting channel ID...")
            self.channel = use_data['channel']
            log.info("[:P] - Success!\n")

        except Exception as channel_err:
            log.info("[X] - Error getting channel ID!")
            log.info(channel_err)

        try:
            log.info("[!] - Getting text message...")
            self.text = use_data['text']
            log.info("[:P] - Success!\n")

        except Exception as text_err:
            log.info("[X] - Error getting text message!")
            log.info(text_err)

        try:
            log.info("[!] - Getting message timestamp...")
            self.ts = use_data['ts']
            log.info("[:P] - Success!\n")

        except Exception as ts_err:
            log.info("[X] - Error getting message timestamp!")
            log.info(ts_err)

    def sanitize(self):
        log.info("[!] - Sanitizing collected messages")
        return [w.upper() for w in self.split_message]

    def analyze_message(self, use_split_message):

        log.info("[!] - Analyzing data..")
        from library import Library
        L = Library()

        log.info("[!] - Getting matched words")
        match_word = (set(L.dictionary()) & set(use_split_message))

        if match_word:
            self.match = [s for s in match_word if s][0]
            log.info(f"[!] - Found word: {self.match}")
            from library import Library

            read_book = Library().bookshelf()
            log.info(f"[:P] - {read_book[self.match]}")

        else:
            log.info("[!] - Unmatched word")

    def delivery_thread(self):
        log.info("[!] - Sending response message...")

        try:
            app.client.chat_postMessage(
                channel=self.channel,
                thread_ts=self.ts,
                text=self.text
            )
        except Exception as slack_reply_err:
            log.error("[X] - Error sending slack message!")
            log.error(slack_reply_err)


if __name__ == "__main__":
    """========== SET LOG =========="""
    log = LogEngine(__name__).log()
    StartEngine()
