from json import dumps
from src.models.enums import BookConditionEnum, CoverEnum

class Portfolio:
    def __init__(self, id, book_id, condition: BookConditionEnum, cover: CoverEnum):
        self.id = id
        self.book_id = book_id
        self.condition = condition
        self.cover = cover

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "condition": self.condition.value if hasattr(self.condition, 'value') else self.condition,
            "cover": self.cover.value if hasattr(self.cover, 'value') else self.cover
        }

    def to_json(self):
        return dumps(self.to_dict())
