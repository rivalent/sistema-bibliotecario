from src.storage.db_manager import DBManager

class DBInitializer:
    def __init__(self):
        self.conn = DBManager()

    def create_tables(self):
        users_table_query = ("""
            CREATE TABLE IF NOT EXISTS users (
                id CHAR(26) PRIMARY KEY,
                name VARCHAR(256) NOT NULL,
                email VARCHAR(512) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                inactive_at DATETIME,
                active BOOLEAN DEFAULT TRUE
            );
        """)

        books_table_query = ("""
            CREATE TABLE IF NOT EXISTS books (
                isbn CHAR(13) PRIMARY KEY,
                title VARCHAR(512) NOT NULL,
                release_year INT NOT NULL,
                summary TEXT,
                author TEXT NOT NULL,
                page_len INT,
                publisher TEXT
            );
        """)

        genre_table_query = """
            CREATE TABLE IF NOT EXISTS genre (
                book_id CHAR(13),
                genre TEXT NOT NULL,
                PRIMARY KEY (book_id, genre),
                FOREIGN KEY (book_id) REFERENCES books(isbn) ON DELETE CASCADE,
                CONSTRAINT check_genre_enum CHECK (genre IN (
                    'academic', 'adult_fiction', 'adventure', 'art', 'autobiography', 'biography', 'business', 'childrens', 
                    'christian', 'christian_fiction', 'classics', 'comedy', 'contemporary', 'crime', 'cultural', 'default', 'distopian',
                    'erotica', 'fantasy', 'fiction', 'food_and_drink', 'graphic_novel', 'health', 'historical', 'historical_fiction', 'history', 'horror', 'humor',
                    'manga_isekai', 'manga_josei', 'manga_seinen', 'manga_shoujo', 'manga_shonen', 'memoir', 'music', 'mystery', 'new_adult', 'nonfiction', 'novels',
                    'paranormal', 'parenting', 'philosophy', 'poetry', 'politics', 'psychology', 'religion', 'romance', 'science', 
                    'science_fiction', 'self_help', 'sequential_art', 'short_stories', 'spirituality', 'sports_and_games', 'suspense',
                    'thriller', 'travel', 'true_crime', 'womens_fiction', 'young_adult'
                ))
            );
        """

        portfolio_table_query = ("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id CHAR(26) PRIMARY KEY,
                book_id CHAR(13),
                condition TEXT NOT NULL,
                cover TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(isbn) ON DELETE CASCADE,
                CONSTRAINT check_portfolio_condition CHECK (condition IN (
                    'perfect', 'good', 'bad', 'useless', 'disable'
                )),
                CONSTRAINT check_cover_enum CHECK (cover IN (
                    'paper', 'hardcover'
                ))
            );
        """)

        loan_table_query = ("""
            CREATE TABLE IF NOT EXISTS loan (
                id CHAR(26) PRIMARY KEY,
                portfolio_id CHAR(26),
                user_id CHAR(26),
                start_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                return_at DATETIME DEFAULT NULL,
                period INT NOT NULL DEFAULT 30,
                loan_condition TEXT,
                return_condition TEXT DEFAULT NULL,
                FOREIGN KEY (portfolio_id) REFERENCES portfolio(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                CONSTRAINT check_loan_start_condition CHECK (loan_condition IN (
                    'perfect', 'good', 'bad', 'useless', 'disable'
                )),
                CONSTRAINT check_loan_return_condition CHECK (return_condition IN (
                    'perfect', 'good', 'bad', 'useless', 'disable'
                ))
            );
        """)

        self.conn.execute_query(users_table_query)
        self.conn.execute_query(books_table_query)
        self.conn.execute_query(genre_table_query)
        self.conn.execute_query(portfolio_table_query)
        self.conn.execute_query(loan_table_query)

if __name__ == "__main__":
    creator = DBInitializer()
    creator.create_tables()
    print("Todas as tabelas foram criadas")
