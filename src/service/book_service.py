import logging
import traceback
from src.repositories.book_repository import BookRepository
from src.repositories.genre_repository import GenreRepository
from src.models.book import Book
from src.models.genre import Genre

class BookService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.genre_repo = GenreRepository()

    def create(self, title, isbn, author, release_year, publisher, page_len, genre_enum, summary=None):
        new_book = None
        try:
            new_book = Book (
                title=title,
                isbn=isbn,
                author=author,
                release_year=release_year,
                publisher=publisher,
                page_len=page_len,
                summary=summary
            )
            self.book_repo.create_book(new_book)

            new_genre_association = Genre (
                book_id=isbn,
                genre=genre_enum
            )
            self.genre_repo.create_genre(new_genre_association)

            logging.debug(f"[BOOK-SERVICE] Created book: {title} with genre {genre_enum}")
            return new_book
            
        except Exception as error:
            logging.error(f"[BOOK-SERVICE] Fail to create: {error} -> {traceback.format_exc()}")

            if new_book:
                logging.warning(f"[BOOK-SERVICE] Rolling back... Deleting orphan book {isbn}")
                self.book_repo.delete_book(isbn)
                
            return None

    def find_by_isbn(self, isbn):
        try:
            book = self.book_repo.get_book_by_id(isbn)

            if not book:
                logging.info(f"[BOOK-SERVICE] Book {isbn} not found")
                return None
            
            logging.debug(f"[BOOK-SERVICE] Found: {book.isbn}")
            return book

        except Exception as error:
            logging.error(f"[BOOK-SERVICE] Fail to find: {error} -> {traceback.format_exc()}")

    def search(self, query, search_type="title"):
        try:
            list_books = []

            if search_type == "title":
                list_books = self.book_repo.get_book_by_title(query)
            elif search_type == "author":
                list_books = self.book_repo.get_book_by_author(query)
            elif search_type == "genre":
                list_books = self.book_repo.get_book_by_genre(query)
            else:
                list_books = self.book_repo.get_book_by_title(query)

            logging.debug(f"[BOOK-SERVICE] Found: {len(list_books)} books")
            return list_books

        except Exception as error:
            logging.error(f"[BOOK-SERVICE] Fail to search: {error}")
            return []

    def update(self, isbn, title, author, publisher):
        try:
            book = self.find_by_isbn(isbn)

            if not book:
                logging.warning(f"[BOOK-SERVICE] Attempt to update non-existent book: {isbn}")
                return None

            book.title = title
            book.author = author
            book.publisher = publisher

            self.book_repo.update_book(book)

            logging.debug(f"[BOOK-SERVICE] Updated: {book.isbn}")
            return book

        except Exception as error:
             logging.error(f"[BOOK-SERVICE] Fail to update: {error}")
             return None

    def delete(self, isbn):
        try:
            self.book_repo.delete_book(isbn)

            logging.debug(f"[BOOK-SERVICE] DELETED Book isbn: {isbn}")
            return True

        except Exception as error:
            logging.error(f"[BOOK-SERVICE] Fail to delete: {error}")
            return False
