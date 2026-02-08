from src.storage.db_manager import DBManager
from src.models.genre import Genre

class GenreRepository:
    def __init__(self):
        self.db = DBManager()

    def create_genre(self, genre_obj: Genre):
        query = """
            INSERT INTO genre (book_id, genre)
            VALUES (?, ?)
        """
        genre_val = getattr(genre_obj.genre, 'value', genre_obj.genre)
        params = (genre_obj.book_id, genre_val)
        self.db.execute_query(query, params)

        return genre_obj

    def get_genre_by_book_id(self, book_id) -> list[Genre]:
        query = "SELECT * FROM genre WHERE book_id = ?"
        params = (book_id, )
        result = self.db.execute_query(query, params)

        items_list = []
        if result:
            for row in result:
               items_list.append(Genre(*row))
        return items_list 

    def delete_genre(self, book_id, genre_input):
        query = "DELETE FROM genre WHERE book_id = ? AND genre = ?"
        genre_val = getattr(genre_input, 'value', genre_input)
        
        params = (book_id, genre_val)
        self.db.execute_query(query, params)
