from json import dumps
from src.models.enums import BookConditionEnum, CoverEnum
from typing import Optional, Union

class Portfolio:
    def __init__(
        self, 
        book_id: str, 
        condition: Union[BookConditionEnum, str],
        cover: Union[CoverEnum, str],
        id: Optional[str] = None,
        title: Optional[str] = None
    ):
        self.id = id
        self.book_id = book_id
        self.condition = condition
        self.cover = cover
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "title": self.title,
            "condition": self.condition.value if hasattr(self.condition, 'value') else self.condition,
            "cover": self.cover.value if hasattr(self.cover, 'value') else self.cover
        }

    def to_json(self):
        return dumps(self.to_dict())
