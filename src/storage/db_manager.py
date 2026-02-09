import sqlite3
from pathlib import Path

class DBManager:
    def __init__(self):
        self.db_path = Path(__file__).parent.parent.parent / 'data.db'
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row 
        
        return conn

    def execute_query(self, query, params=None):
        try:
            with self.get_connection() as conn:
                if params:
                    cursor = conn.execute(query, params)
                else:
                    cursor = conn.execute(query)

                return cursor.fetchall()

        except Exception as e:
            print(f"Erro ao executar query: {e}")
            raise e