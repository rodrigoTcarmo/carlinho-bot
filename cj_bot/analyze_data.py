import logging
import time
from Logs.log_engine import LogEngine
from data_fetch_module.data_fetch import SlackDataHelper


class StartAnalyze:
    def __init__(self, get_payload, get_user_info, get_pagcloud_docs):
        """========== START LOG ENGINE =========="""
        self.log = LogEngine(__name__).log_bot()

        self.payload = get_payload
        self.log.info("[!] - Payload data collected from Slack message:")
        self.log.info(self.payload)

        self.user_info = get_user_info
        self.log.info("[!] - User information:")
        self.log.info(self.user_info)

        self.log.info("[!] - Initializing data helper class...")
        time.sleep(0.1)
        self.i_data_helper = SlackDataHelper()

        self.pagcloud_docs = get_pagcloud_docs
        self.sanitized_data = None
        self.fetch_pagpedia = None
        self.message_text = None
        self.payload_dict = None
        self.suggest_docs = None
        self.match_data = None
        self.search_limit = 4
        self.channel = None
        self.name_id = None
        self.blocks = None
        self.ts = None

    def start_analyze(self):
        # Set each payload key in variables
        self.log.info("[!] - Setting all payload data in variables...")
        try:
            self.payload_dict = self.set_data()
            self.log.info("[OK] - Done!\n")
        except Exception as set_payload_data_err:
            self.log.info("[ERROR] - Error while setting payload data!")
            self.log.info(set_payload_data_err)
            return False

        # Transform Slack message into a list of each word
        self.log.info("[!] - Transforming the message into a list...")
        try:
            self.message_text = self.payload_dict['text'].split()
            self.log.info("[OK] - Done!\n")
        except Exception as transform_text_into_list_err:
            self.log.info("[ERROR] - Error while transforming the message into a list!")
            self.log.info(transform_text_into_list_err)
            return False

        # Get channel ID and set a variable for it
        self.log.info("[!] - Getting channel ID...")
        try:
            self.channel = self.payload_dict['channel']
            self.log.info("[OK] - Done!\n")
        except Exception as get_channel_err:
            self.log.info("[ERROR] - Error while getting channel ID!")
            self.log.info(get_channel_err)
            return False

        # Get timestamp of message that was sent, to reply in thread
        self.log.info("[!] - Getting timestamp...")
        try:
            self.ts = self.payload_dict['ts']
            self.log.info("[OK] - Done!\n")
        except Exception as get_ts_err:
            self.log.info("[ERROR] - Error while getting timestamp!")
            self.log.info(get_ts_err)
            return False

        # Get the user of message that was sent
        self.log.info("[!] - Getting user...")
        try:
            self.name_id = self.payload_dict['user']
            self.log.info("[OK] - Done!\n")
        except Exception as get_user_err:
            self.log.info("[ERROR] - Error while getting user!")
            self.log.info(get_user_err)
            return False

        # Remove common words to speedup bot processing
        self.log.info("[!] - Sanitizing message...")
        try:
            self.sanitized_data = self.sanitize_data()
            self.log.info("[OK] - Done!\n")
        except Exception as sanitize_err:
            self.log.info("[ERROR] - Error while sanitizing message!")
            self.log.info(sanitize_err)
            return False

        self.log.info("[!] - Searching pagcloud documentation...")
        try:
            self.match_data = self.search_data()
            self.log.info("[OK] - Done!\n")
        except Exception as search_pagcloud_docs_err:
            self.log.info("[ERROR] - Error while searching pagcloud documentation!")
            self.log.info(search_pagcloud_docs_err)
            return False

        if self.match_data:
            self.log.info('[!] - Matching words:')
            self.log.info(self.match_data.keys())
            self.log.info("[!] - Organizing reply message...")
            try:
                self.organize_data()
                self.log.info("[OK] - Message organized! Ready to send!\n")
            except Exception as organize_message_err:
                self.log.info("[ERROR] - Error while organizing message!")
                self.log.info(organize_message_err)
                return False

            return self.serial_data()

        else:
            self.log.info("[FINISH] - No matching words were found!\n")
            return False

    def set_data(self):
        return self.i_data_helper.set_dict(payload_data=self.payload)

    def sanitize_data(self):
        return self.i_data_helper.sanitize(slack_message=self.message_text)

    def search_data(self):
        return self.i_data_helper.match_search(sanitized_data=self.sanitized_data, pagpedia_index=self.pagcloud_docs)

    def suggest_data(self):
        self.suggest_docs = {}

        if 'location' not in self.suggest_docs:
            self.suggest_docs['location'] = []

        if 'title' not in self.suggest_docs:
            self.suggest_docs['title'] = []

        if 'text' not in self.suggest_docs:
            self.suggest_docs['text'] = []

        while len(self.suggest_docs['location']) < self.search_limit:

            for i in self.match_data:
                item_dict = self.match_data[i]

                shortest_location = min(item_dict['location'], key=len)
                shortest_location_index = item_dict['location'].index(shortest_location)

                title = item_dict['title'][shortest_location_index]
                text = item_dict['text'][shortest_location_index]

                item_dict['location'].pop(shortest_location_index)
                item_dict['title'].pop(shortest_location_index)
                item_dict['text'].pop(shortest_location_index)

                if shortest_location not in self.suggest_docs['location']:
                    self.suggest_docs['location'].append(shortest_location)

                if title not in self.suggest_docs['title']:
                    self.suggest_docs['title'].append(title)

                if text not in self.suggest_docs['text']:
                    self.suggest_docs['text'].append(text)

                if len(self.suggest_docs['location']) == self.search_limit:
                    break

        return self.suggest_docs

    def organize_data(self):
        base_url = 'https://docs.cloud.intranet.pags/v1/'
        get_suggest_data = self.suggest_data()
        suggest_doc = base_url + get_suggest_data['location'].pop(0)
        nl = '\n'
        jira_link = f"<{'https://jiraps.atlassian.net/servicedesk/customer/portal/146'}|ABRIR CHAMADO>"
        self.blocks = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Olá {self.user_info['user']['real_name']}! Não esqueça de abrir seu chamado para o time "
                        f"San Fierro!"
            }
        }]

        self.blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Abrir chamado"
                    },
                    "style": "primary",
                    "value": "click_card_opener",
                    "url": "https://jiraps.atlassian.net/servicedesk/customer/portal/146",
                    "action_id": "button-action"
                }
            ]
        })

        self.blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Será que essas documentações ajudam?"
            }
        })

        for build_r in range(self.search_limit):
            print('TITLE QUE RESTA:', get_suggest_data['title'])
            try:
                reply_msg = f"<{suggest_doc}|{get_suggest_data['title'].pop(0)}>\n{get_suggest_data['text'].pop(0)[0:100].replace(u'¶', nl)}...\n"
                self.blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": reply_msg
                        }
                    })
                self.blocks.append(
                    {
                        "type": 'divider'
                    })
            except IndexError:
                self.log.info('[!] - One or more lists are smaller than expected! Ignoring...')

            except Exception as general_list_err:
                self.log.info('[ERROR] - Build reply error!')
                self.log.info(general_list_err)

    def serial_data(self):
        s_data = [self.channel, self.ts, self.blocks, self.log]
        return s_data
