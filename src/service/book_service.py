import logging
import traceback
from src.repositories.book_repository import BookRepository
from src.repositories.genre_repository import GenreRepository
from src.models.book import Book
from src.models.genre import Genre
from src.schemas.book_schema import BookUpdate

class BookService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.genre_repo = GenreRepository()

    def create(self, title: str, isbn: str, author: str, release_year: int, publisher: str, page_len: int, genre_enum: str, summary: str = None):
        try:
            title = title.strip()
            isbn = isbn.strip()
            author = author.strip()
            publisher = publisher.strip()
            genre_enum = genre_enum.strip().lower()
            
            if summary:
                summary = summary.strip()
            
            if len(isbn) != 13:
                logging.warning(f"[BOOK-SERVICE] Invalid ISBN length: {len(isbn)}")
                raise ValueError("ISBN must have exactly 13 characters")

            new_book = Book(
                title=title,
                isbn=isbn,
                author=author,
                release_year=release_year,
                publisher=publisher,
                page_len=page_len,
                summary=summary
            )
            
            self.book_repo.create_book(new_book)

            new_genre_association = Genre(
                book_id=isbn,
                genre=genre_enum
            )
            self.genre_repo.create_genre(new_genre_association)

            logging.debug(f"[BOOK-SERVICE] Created book: {title} with genre {genre_enum}")
            return new_book
            
        except Exception as error:
            logging.error(f"[BOOK-SERVICE] Fail to create: {error} -> {traceback.format_exc()}")
            logging.warning(f"[BOOK-SERVICE] Rolling back... Deleting orphan book {isbn}")
            self.book_repo.delete_book(isbn)
            
            return None

    def find_by_isbn(self, isbn: str):
        try:
            isbn = isbn.strip()
            book = self.book_repo.get_book_by_id(isbn)

            if not book:
                logging.info(f"[BOOK-SERVICE] Book {isbn} not found")
                return None

            logging.debug(f"[BOOK-SERVICE] Found: {book.isbn}")
            return book

        except Exception as error:
            logging.error(f"[BOOK-SERVICE] Fail to find: {error} -> {traceback.format_exc()}")
            return None

    def search(self, query: str, search_type: str = "title"):
        try:
            list_books = []
            query = query.strip()
            search_type = search_type.strip().lower()

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

    def update(self, isbn: str, update_data: BookUpdate):
        try:
            isbn = isbn.strip()
            book = self.find_by_isbn(isbn)

            if not book:
                logging.warning(f"[BOOK-SERVICE] Attempt to update non-existent book: {isbn}")
                return None

            if update_data.title is not None:
                book.title = update_data.title.strip()

            if update_data.author is not None:
                book.author = update_data.author.strip()

            if update_data.publisher is not None:
                book.publisher = update_data.publisher.strip()

            if update_data.release_year is not None:
                book.release_year = update_data.release_year

            if update_data.page_len is not None:
                book.page_len = update_data.page_len

            if update_data.summary is not None:
                book.summary = update_data.summary.strip()

            self.book_repo.update_book(book)

            if update_data.genre is not None:
                clean_genre = update_data.genre.strip().lower()
                book.genre_enum = clean_genre
                
                self.genre_repo.update_genre(isbn, clean_genre)

            logging.debug(f"[BOOK-SERVICE] Updated: {book.isbn}")
            return book

        except Exception as error:
             logging.error(f"[BOOK-SERVICE] Fail to update: {error} -> {traceback.format_exc()}")
             return None

    def delete(self, isbn: str):
        try:
            isbn = isbn.strip()

            if not self.find_by_isbn(isbn):
                return False

            self.book_repo.delete_book(isbn)
            logging.debug(f"[BOOK-SERVICE] DELETED Book isbn: {isbn}")
            return True

        except Exception as error:
            logging.error(f"[BOOK-SERVICE] Fail to delete: {error}")
            return False