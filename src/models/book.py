from json import dumps
from typing import Optional

class Book:
    def __init__(
        self, 
        isbn: str, 
        title: str, 
        release_year: int, 
        author: str, 
        page_len: int,
        publisher: str,
        summary: Optional[str] = None 
    ):
        self.isbn = isbn
        self.title = title
        self.release_year = release_year
        self.author = author
        self.page_len = page_len
        self.publisher = publisher
        self.summary = summary

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
