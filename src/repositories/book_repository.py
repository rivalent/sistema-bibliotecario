from src.storage.db_manager import DBManager
from src.models.book import Book
import logging

class BookRepository:
    def __init__(self):
        self.db = DBManager()

    def map_row_to_book(self, row) -> Book:
        return Book(
            isbn = row["isbn"],
            title = row["title"],
            release_year = row["release_year"],
            summary = row["summary"],
            author = row["author"],
            page_len = row["page_len"],
            publisher = row["publisher"]
        )

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
            logging.debug(f"[BOOK-REPOSITORY] Create successfully: {book.title}")
            return book

        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to create: {error}")
            raise error

    def get_book_by_id(self, isbn) -> Book:
        try:
            query = """
                SELECT title, isbn, author, release_year, publisher, page_len, summary
                FROM books 
                WHERE isbn = ?
            """
            params = (isbn,)
            result = self.db.execute_query(query, params)

            if result:
                row = result[0]
                return self.map_row_to_book(row)

            logging.debug(f"[BOOK-REPOSITORY] Book search not found: {isbn}")
            return None

        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get book Id: {error}")
            raise error

    def get_book_by_title(self, book_title) -> list[Book]:
        try:
            query = """
                SELECT title, isbn, author, release_year, publisher, page_len, summary 
                FROM books
                WHERE title LIKE ?
            """
            params = (f"%{book_title}%",)
            result = self.db.execute_query(query, params)

            books_list = []
            if result:
                for row in result:
                    books_list.append(self.map_row_to_book(row))

            logging.debug(f"[BOOK-REPOSITORY] returned : {len(books_list)} books")
            return books_list
    
        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get title: {error}")
            raise error

    def get_book_by_author(self, book_author) -> list[Book]:
        try:
            query = """
                SELECT title, isbn, author, release_year, publisher, page_len, summary 
                FROM books
                WHERE author LIKE ?
            """
            params = (f"%{book_author}%",)
            result = self.db.execute_query(query, params)

            books_list = []
            if result:
                for row in result:
                    books_list.append(self.map_row_to_book(row))

            logging.debug(f"[BOOK-REPOSITORY] returned: {len(books_list)} books")
            return books_list

        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get author: {error}")
            raise error
    
    def get_book_by_genre(self, book_genre) -> list[Book]:
        try:
            query = """
                SELECT b.title, b.isbn, b.author, b.release_year, b.publisher, b.page_len, b.summary 
                FROM books b
                JOIN genre g ON b.isbn = g.book_id
                WHERE g.genre LIKE ?
            """
            params = (f"%{book_genre}%",)
            result = self.db.execute_query(query, params)

            books_list = []
            if result:
                for row in result:
                    books_list.append(self.map_row_to_book(row))

            logging.debug(f"[BOOK-REPOSITORY] returned: {len(books_list)} books")
            return books_list
        
        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to get genre: {error}")
            raise error
    
    def update_book(self, book: Book):
        try:
            query = """
                UPDATE books 
                SET title = ?, release_year = ?, summary = ?, author = ?, page_len = ?, publisher = ?
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
            logging.debug(f"[BOOK-REPOSITORY] Updated: {book.isbn}")

        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to update: {error}")
            raise error

    def delete_book(self, isbn):
        try:
            query = "DELETE FROM books WHERE isbn = ?"
            params = (isbn,)
            self.db.execute_query(query, params)
            logging.debug(f"[BOOK-REPOSITORY] deleted book: {isbn}")
        except Exception as error:
            logging.error(f"[BOOK-REPOSITORY] Fail to delete: {error}")
            raise error
