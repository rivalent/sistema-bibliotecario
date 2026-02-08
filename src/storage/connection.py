import sqlite3
from pathlib import Path

class DBConnection:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / 'data.db'

    def get_connection(self):
        return sqlite3.connect(self.db_path)