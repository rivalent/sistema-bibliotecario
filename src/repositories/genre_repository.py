import logging
import traceback
from src.storage.db_manager import DBManager
from src.models.genre import Genre

class GenreRepository:
    def __init__(self):
        self.db = DBManager()

    def map_row_to_genre(self, row) -> Genre:
        return Genre(
            book_id=row['book_id'],
            genre=row['genre']
        )

    def create_genre(self, genre_obj: Genre):
        try:
            query = """
                INSERT INTO genre (book_id, genre)
                VALUES (?, ?)
            """
            genre_val = getattr(genre_obj.genre, 'value', genre_obj.genre)
            
            params = (genre_obj.book_id, genre_val)
            self.db.execute_query(query, params)

            logging.debug(f"[GENRE-REPO] Linked genre '{genre_val}' to Book {genre_obj.book_id}")
            return genre_obj

        except Exception as error:
            logging.error(f"[GENRE-REPO] Fail to create genre: {error}")
            raise error

    def get_genres_by_book_id(self, book_id) -> list[Genre]:
        try:
            query = "SELECT book_id, genre FROM genre WHERE book_id = ?"
            params = (book_id, )
            result = self.db.execute_query(query, params)

            items_list = []
            if result:
                for row in result:
                    items_list.append(self.map_row_to_genre(row))
            
            return items_list

        except Exception as error:
            logging.error(f"[GENRE-REPO] Fail to get genres: {error}")
            return []

    def delete_all_genres_by_book(self, book_id):
        try:
            query = "DELETE FROM genre WHERE book_id = ?"
            self.db.execute_query(query, (book_id,))
            logging.debug(f"[GENRE-REPO] Cleared genres for Book {book_id}")

        except Exception as error:
            logging.error(f"[GENRE-REPO] Fail to delete genres: {error}")
            raise error

    def delete_specific_genre(self, book_id, genre_input):
        try:
            query = "DELETE FROM genre WHERE book_id = ? AND genre = ?"
            genre_val = getattr(genre_input, 'value', genre_input)
            
            params = (book_id, genre_val)
            self.db.execute_query(query, params)
            logging.debug(f"[GENRE-REPO] Removed genre '{genre_val}' from Book {book_id}")

        except Exception as error:
            logging.error(f"[GENRE-REPO] Fail to delete specific genre: {error}")
            raise error