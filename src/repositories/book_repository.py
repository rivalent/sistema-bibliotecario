from src.storage.db_manager import DBManager
from src.models.book import Book
import logging

class BookRepository:
    def __init__(self):
        self.db = DBManager()
    
    def create_book(self, book: Book):
        try:
            query = """
                INSERT INTO books (isbn, title, release_year, summary, author, page_len, publisher)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                book.isbn,
                book.title,
                book.release_year,
                book.summary,
                book.author,
                book.page_len,
                book.publisher
            )

            self.db.execute_query(query, params)
            logging.debug(f"[BOOK-REPOSITORY] Create sucefully: {book}")
            return book

        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to create: {error}")
            raise error

    def get_book_by_id(self, isbn) -> Book:
        try:
            query = "SELECT * from books WHERE isbn = ?"
            params = (isbn,)
            result = self.db.execute_query(query,params)

            if result:
                row = result[0]
                book = Book(*row)

                return book
            logging.debug(f"[BOOK-REPOSITORY] Book search: {book}")
            return None

        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get book Id: {error}")
            raise error

    def get_book_by_title(self, book_title) -> list[Book]:
        try:
            query = "SELECT * FROM books WHERE title LIKE ?"
            params = (f"%{book_title}%",)
            result = self.db.execute_query(query, params)

            books_list = []
            if result:
                for row in result:
                    books_list.append(Book(*row))
            logging.debug(f"[BOOK-REPOSITORY] returned : {len(books_list)} books")
            return books_list
    
        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get title: {error}")
            raise error

    def get_book_by_author(self, book_author) -> list[Book]:
        try:
            query = "SELECT * FROM books WHERE author LIKE ?"
            params = (f"%{book_author}%",)
            result = self.db.execute_query(query, params)

            books_list = []
            if result:
                for row in result:
                    books_list.append(Book(*row))
            logging.debug(f"[BOOK-REPOSITORY] returned: {len(books_list)} books")
            return books_list

        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get author: {error}")
            raise error
    
    def get_book_by_genre(self, book_genre) -> list[Book]:
        try:
            query = """
                SELECT b.* FROM books b
                JOIN genre g ON b.isbn = g.book_id
                WHERE g.genre LIKE ?
            """
            params = (f"%{book_genre}%",)
            result = self.db.execute_query(query, params)

            books_list = []
            if result:
                for row in result:
                    books_list.append(Book(*row))
            logging.debug(f"[BOOK-REPOSITORY] returned: {len(books_list)} books")
            return books_list
        
        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get genre: {error}")
            raise error
    
    def update_book(self, book:Book):
        query = """
            UPDATE books SET title = ?, release_year = ?, summary = ?, author = ?, page_len = ?, publisher = ?
            WHERE isbn = ?
        """
        params = (
            book.title,
            book.release_year,
            book.summary,
            book.author,
            book.page_len,
            book.publisher,
            book.isbn
        )
        self.db.execute_query(query, params)

    def delete_book(self, isbn):
        try:
            query = "DELETE FROM books WHERE isbn = ?"
            params = (isbn,)
            self.db.execute_query(query, params)
            logging.debug(f"[BOOK-REPOSITORY] deleted book: {isbn}")
        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to delete: {error}")
            raise error
