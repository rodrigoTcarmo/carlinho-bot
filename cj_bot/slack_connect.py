# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Just like a chatbot, this code creates a communication with slack using SocketMODE (official slack), here we use
slack bolt too, automating tasks and following best practices.

Author: Rodrigo Carmo
EC: San Fierro

"""
import os
import sys
import requests
from slack_bolt import App
from Logs.log_engine import LogEngine
from dotenv import load_dotenv
from cj_bot.analyze_data import StartAnalyze
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
app = App(token=SLACK_BOT_TOKEN)
log = LogEngine(__name__).log_bot()


def fetch_docs_pagcloud():
    try:
        log.info('[!] - Fetching pagcloud docs...')
        pagcloud_url = 'https://docs.cloud.intranet.pags/v1/search/search_index.json'
        fetch_json = requests.get(url=pagcloud_url).json()
        log.info('[!] - Pagcloud data fetched successfully!')
        return fetch_json

    except Exception as fetch_docs_index_err:
        log.info(fetch_docs_index_err)


pagpedia_docs = fetch_docs_pagcloud()


class SlackEngine:

    def __init__(self):
        try:
            handler = SocketModeHandler(app, SLACK_APP_TOKEN)
            log.info("[!] - Running handler...")
            handler.start()
        except Exception as start_handler_err:
            sys.stderr.write("[ERROR] - Error trying to start slack handler!")
            sys.stderr.write(str(start_handler_err))

    @app.event("message")
    def listen_messages(payload):

        if 'thread_ts' not in payload:
            app.client.reactions_add(channel=payload['channel'], name="eyes", timestamp=payload['ts'])
            user_info = app.client.users_info(user=payload['user'])
            process = StartAnalyze(get_payload=payload,
                                   get_user_info=user_info,
                                   get_pagcloud_docs=pagpedia_docs).start_analyze()

            if process:
                SendMessage(process[3]).send_message(s_channel=process[0], s_ts=process[1], s_blocks=process[2])

    @app.action("button-action")
    def button_handler(payload, ack, body, logger):
        ack()
        log.info('[!] - Button selected!')
        log.info(body)
        log.info('[FINISH] - End!\n')


    def test(self):
        pass
class SendMessage:

    def __init__(self, s_logs):
        self.log = s_logs

    def send_message(self, s_channel, s_ts, s_blocks):
        self.log.info("[!] - Sending slack message...")
        try:
            app.client.chat_postMessage(
                channel=s_channel,
                thread_ts=s_ts,
                text="Encontrei algumas documentações aqui, o que acha?",
                blocks=s_blocks)
            self.log.info("[OK] - Message sent!")
            self.log.info("[FINISH] - End!\n")
        except Exception as slack_reply_err:
            self.log.info("[X] - Error sending slack message!\n")
            self.log.info(str(slack_reply_err))
            self.log.info('\n')
