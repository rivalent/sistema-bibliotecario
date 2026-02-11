from json import dumps
from src.models.enums import GenreEnum
from typing import Union

class Genre:
    def __init__(
        self, 
        book_id: str, 
        genre: Union[GenreEnum, str]
    ):
        self.book_id = book_id
        self.genre = genre
    
    def to_dict(self):
        return {
            "book_id": self.book_id,
            "genre": self.genre.value if hasattr(self.genre, 'value') else self.genre
        }

    def to_json(self):
        return dumps(self.to_dict())
