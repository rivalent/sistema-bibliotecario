from json import dumps

class Book:
    # mapear de 1 pra 1 em dicionário
    def __init__(self, isbn, title, release_year, author, summary=None, page_len=None, publisher=None):
        self.isbn = isbn
        self.title = title
        self.release_year = release_year
        self.summary = summary
        self.author = author
        self.page_len = page_len
        self.publisher = publisher

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "release_year": self.release_year,
            "summary": self.summary,
            "author": self.author,
            "page_len": self.page_len,
            "publisher": self.publisher
        }

    def to_json(self):
        return dumps(self.to_dict())
