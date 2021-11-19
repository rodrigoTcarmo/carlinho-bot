
class Library:
    def __init__(self):
        self.dict_words = ['JIRA', 'AWS', 'JENKINS']
        self.books = {
            "JIRA": "Encontrei isso aqui sobre o JIRA",
            "AWS": "Sobre AWS encotnrei isso",
            "JENKINS": "Ja o JENKINS talvez isso ajude"
        }

    def dictionary(self):
        return self.dict_words

    def bookshelf(self):
        return self.books
