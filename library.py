import requests


class Library:
    def __init__(self):
        url = "https://docs.cloud.intranet.pags/v1/search/search_index.json"
        self.search_data = requests.get(url=url).json()
        self.doc_location = []

    def dictionary(self):
        for d in self.search_data["docs"]:
            self.doc_location.append(d["location"])
        return self.doc_location

    def bookshelf(self):
        return self.books
