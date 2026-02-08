from enum import Enum

class GenreEnum(Enum):
    ADVENTURE = "adventure"
    ROMANCE = "romance"
    FANTASY = "fantasy"
    SCI_FI = "sci_fi"
    HISTORY = "history"
    HORROR = "horror"
    DISTOPIAN = "distopian"
    BIOGRAPHY = "biography"
    SELF_HELP = "self_help"
    MEMORY = "memory"
    TRUE_CRIME = "true_crime"
    POETRY = "poetry"
    GRAPHIC_NOVEL = "graphic_novel"
    COMEDY = "comedy"

class BookConditionEnum(Enum):
    PERFECT = "perfect"
    GOOD = "good"
    BAD = "bad"
    USELESS = "useless"
    DISABLE = "disable"

class CoverEnum(Enum):
    PAPER = "paper"
    HARDCOVER = "hardcover"