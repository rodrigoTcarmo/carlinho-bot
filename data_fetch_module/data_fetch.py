"""
The main objective of this code, is to deliver an easy way to process and filter data we receive from slack app.
Author: Rodrigo Carmo
EC: San Fierro
"""

import re
import sys
import nltk
import requests
from nltk.corpus import stopwords


class SlackDataHelper:
    def __init__(self):
        """---- set_data variables ----"""
        self.client_msg_id = None
        self.type = None
        self.text = None
        self.user = None
        self.ts = None
        self.channel = None
        self.event_ts = None
        self.team = None
        self.blocks = None
        self.channel_type = None
        self.payload_dict = {}

        """---- pagcloud_index ----"""
        self.pagcloud_url = None
        self.fetch_json = None
        self.doc_location = []

        self.sanitized_text = []

        self.match_dict = {}
        self.get_location_result = None
        self.match = None

        sys.stdout.write("Downloading nltk stopwords...\n")
        try:
            nltk.download('stopwords', quiet=True)
            sys.stdout.write("Done!\n")
        except Exception as download_nltk_spwds:
            sys.stderr.write("Error while downloading nltk stopwords!\n")
            sys.stderr.write(str(download_nltk_spwds))

    def set_dict(self, payload_data):
        sys.stdout.write("Collecting data\n")
        try:
            self.client_msg_id = payload_data['client_msg_id']
            self.payload_dict['client_msg_id'] = self.client_msg_id
            sys.stdout.write('Client message id set!\n')

        except Exception as client_msg_id_err:
            sys.stderr.write('Error getting client_message_id from payload!\n')
            sys.stderr.write(str(client_msg_id_err))
            sys.stderr.write('\n')

        try:
            self.type = payload_data['type']
            self.payload_dict['type'] = self.type
            sys.stdout.write('Type set!\n')

        except Exception as type_err:
            sys.stderr.write('Error getting type from payload!\n')
            sys.stderr.write(str(type_err))
            sys.stderr.write('\n')

        try:
            self.text = payload_data['text']
            self.payload_dict['text'] = self.text
            sys.stdout.write("Text set!\n")

        except Exception as text_err:
            sys.stderr.write("Error getting text message from payload!\n")
            sys.stderr.write(str(text_err))
            sys.stderr.write('\n')

        try:
            self.user = payload_data['user']
            self.payload_dict['user'] = self.user
            sys.stdout.write("User set!\n")

        except Exception as user_err:
            sys.stderr.write("Error getting user from payload!\n")
            sys.stderr.write(str(user_err))
            sys.stderr.write('\n')

        try:
            self.ts = payload_data['ts']
            self.payload_dict['ts'] = self.ts
            sys.stdout.write("Ts (timestamp) set!\n")

        except Exception as ts_err:
            sys.stderr.write("Error getting ts (timestamp) from payload!\n")
            sys.stderr.write(str(ts_err))
            sys.stderr.write('\n')

        try:
            self.team = payload_data['team']
            self.payload_dict['team'] = self.team
            sys.stdout.write('Team set!\n')

        except Exception as team_err:
            sys.stderr.write('Error getting team from payload!\n')
            sys.stderr.write(str(team_err))
            sys.stderr.write('\n')

        try:
            self.blocks = payload_data['blocks']
            self.payload_dict['blocks'] = self.blocks
            sys.stdout.write('Blocks set!\n')

        except Exception as blocks_err:
            sys.stderr.write('Error getting blocks from payload!\n')
            sys.stderr.write(str(blocks_err))
            sys.stderr.write('\n')

        try:
            self.channel = payload_data['channel']
            self.payload_dict['channel'] = self.channel
            sys.stdout.write("Channel set!\n")

        except Exception as channel_err:
            sys.stderr.write("Error getting channel ID from payload!\n")
            sys.stderr.write(str(channel_err))
            sys.stderr.write('\n')

        try:
            self.event_ts = payload_data['event_ts']
            self.payload_dict['event_ts'] = self.event_ts
            sys.stdout.write('Event_ts set!\n')

        except Exception as event_ts_err:
            sys.stderr.write('Error getting event_ts from payload!\n')
            sys.stderr.write(str(event_ts_err))
            sys.stderr.write('\n')

        try:
            self.channel_type = payload_data['channel_type']
            self.payload_dict['channel_type'] = self.channel_type
            sys.stdout.write('Channel_type set!\n\n')

        except Exception as channel_type_err:
            sys.stderr.write('Error getting channel_type from payload!\n')
            sys.stderr.write(str(channel_type_err))
            sys.stderr.write('\n')

        return self.payload_dict

    def sanitize(self, slack_message):
        sys.stdout.write("[!] - Sanitizing collected messages\n")
        dataset = []
        common_words = ["galera", "boa", "bom", "tarde", "dia", "noite", "pessoal", "todos", "ajudar", "podem",
                      "problema", "alguem", "ajuda", "pode", "fala", "tudo"]

        for message_word in slack_message:
            sanitized_message_word = ''.join(e for e in message_word if e.isalnum())
            dataset.append(sanitized_message_word)

        s_dataset = [lwr_string.lower() for lwr_string in dataset]
        removed_stop_words = [s for s in s_dataset if s not in stopwords.words('portuguese')]
        removed_common_words = [c for c in removed_stop_words if c not in common_words]

        self.sanitized_text = [w for w in removed_common_words]

        sys.stdout.write(f'Sanitized word: {self.sanitized_text}\n')

        return self.sanitized_text

    def match_search(self, sanitized_data, pagpedia_index):
        for slack_text in sanitized_data:
            for doc_all in pagpedia_index["docs"]:
                self.get_location_result = re.finditer(f'^{slack_text}/|/{slack_text}/', doc_all['location'])

                for i in self.get_location_result:

                    if slack_text in self.match_dict:

                        if not isinstance(self.match_dict[slack_text]['location'], list):
                            self.match_dict[slack_text]['location'] = [self.match_dict[slack_text]['location']]

                        self.match_dict[slack_text]['location'].append(i.string)

                        if not isinstance(self.match_dict[slack_text]['title'], list):
                            self.match_dict[slack_text]['title'] = [self.match_dict[slack_text]['title']]

                        self.match_dict[slack_text]['title'].append(doc_all['title'])

                        if not isinstance(self.match_dict[slack_text]['text'], list):
                            self.match_dict[slack_text]['text'] = [self.match_dict[slack_text]['text']]

                        self.match_dict[slack_text]['text'].append(doc_all['text'])

                    else:
                        self.match_dict[slack_text] = {}
                        self.match_dict[slack_text]['location'] = i.string
                        self.match_dict[slack_text]['title'] = doc_all['title']
                        self.match_dict[slack_text]['text'] = doc_all['text']

        return self.match_dict

    def pagcloud_index(self, only_location):
        self.pagcloud_url = 'https://docs.cloud.intranet.pags/v1/search/search_index.json'
        self.fetch_json = requests.get(url=self.pagcloud_url).json()

        if only_location:
            for search_pagpedia in self.fetch_json["docs"]:
                self.doc_location.append(search_pagpedia["location"])

            return self.doc_location

        else:
            return self.fetch_json
