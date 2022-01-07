import requests
import re
import nltk


class FetchData:
    def __init__(self):
        # url = "https://docs.cloud.intranet.pags/v1/search/search_index.json"

        self.doc_location = []
        # self.search_data = requests.get(url=url).json()
        self.word = "Fala galera, boa tarde! Podem me ajudar com a workspaces? Estamos com alguns problemas no jenkins e no github aws".split()
        # self.word = "workspaces jenkins github aws".split()
        self.temp_word = ""
        self.match_dict = {}
        self.sanitize_text = []
        self.get_result = None

    def clear_var(self):
        self.temp_word = ""
        return self.temp_word

    def sanitize(self):
        dataset = []
        stop_words = ["fala", "galera", "boa", "bom", "tarde", "dia", "noite", "pessoal", "todos", "ajudar", "podem",
                      "problema"]

        for message_word in self.word:
            sanitized_message_word = ''.join(e for e in message_word if e.isalnum())
            dataset.append(sanitized_message_word)
            # self.sanitize_text.append(sanitized_message_word)

        from nltk.corpus import stopwords
        # nltk.download('stopwords')

        self.sanitize_text = [s for s in dataset if s not in stopwords.words('portuguese')]
        print(self.sanitize_text)
        return self.sanitize_text

    def fetch_data(self):
        for slack_text in FetchData().sanitize():
            for search in FetchData().get_json():
                self.get_result = re.finditer(f'^{slack_text}/|/{slack_text}/', search)

                for i in self.get_result:
                    if slack_text in self.match_dict:
                        if not isinstance(self.match_dict[slack_text], list):
                            self.match_dict[slack_text] = [self.match_dict[slack_text]]

                        self.match_dict[slack_text].append(i.string)

                    else:
                        self.match_dict[slack_text] = i.string

        print(self.match_dict)

    def get_json(self):
        # for search_location in self.search_data["docs"]:
        #     self.doc_location.append(search_location["location"])

        # self.doc_location = ['bla/jenkins/#1-falha-unable-to-connect',
        #                      'workspaces/troubleshooting/#2-falha-unrecognized-user',
        #                      'blu/github/#2-falha-unrecognized-user',
        #                      'blo/aws/#2-falha-unrecognized-user',
        #                      'aaa/jenkins/sdsdsdsdsd/dsdsdsds']

        with open("list_test.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.doc_location.append(line.strip())

        return self.doc_location


if __name__ == "__main__":
    # FetchData().get_json()
    FetchData().fetch_data()
