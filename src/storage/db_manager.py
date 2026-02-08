from src.storage.connection import DBConnection

class DBManager:
    def __init__(self):
        self.db_instance = DBConnection()

    def execute_query(self, query, params=None):
        try:
            with self.db_instance.get_connection() as conn:
                if params:
                    cursor = conn.execute(query, params)
                else:
                    cursor = conn.execute(query)

                return cursor.fetchall()

        except Exception as e:
            print(f"Erro ao executar query: {e}")
            raise e