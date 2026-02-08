from src.storage.db_manager import DBManager
from src.models.user import User

class UserRepository:
    def __init__(self):
        self.db = DBManager()

    def create_user(self, user: User):
        query = """
            INSERT INTO users (id, name, email, created_at, inactive_at, active) 
            VALUES (?, ?, ?, ?, ?, ?)
        """

        params = (
            user.id,
            user.name,
            user.email,
            user.created_at,
            user.inactive_at,
            user.active
        )

        self.db.execute_query(query, params)
        return user
    
    def get_all_users(self) -> list[User]:
        query = "SELECT * FROM users"
        result = self.db.execute_query(query)

        users_list = []
        if result:
            for row in result:
                users_list.append(User(*row))
        return users_list

    def get_user_by_id(self, user_id) -> User:
        query = "SELECT * FROM users WHERE id = ?"
        params = (user_id,)
        result = self.db.execute_query(query, params)

        if result:
            row = result[0]
            user = User(*row)

            return user

        return None

    def get_user_by_name(self, user_name) -> list[User]:
        query = "SELECT * FROM users WHERE name LIKE ?"
        params = (f"%{user_name}%",)
        result = self.db.execute_query(query, params)

        users_list = []
        if result:
            for row in result:
                users_list.append(User(*row))
        return users_list
    
    def get_user_by_email(self, user_email) -> User:
        query = "SELECT * FROM users WHERE email = ?"
        params = (user_email,)
        result = self.db.execute_query(query, params)

        if result:
            row = result[0]
            user = User(*row)
            return user

        return None
    
    def update_user(self, user:User):
        if user.active:
            user.inactive_at = None

        query = "UPDATE users SET name = ?, email = ?, active = ?, inactive_at = ? WHERE id = ?"
        params = (
            user.name,
            user.email,
            user.active,
            user.inactive_at,
            user.id
        )

        self.db.execute_query(query, params)

    def delete_user(self, user_id):
        query = "UPDATE users SET active = 0, inactive_at = datetime('now') WHERE id = ?"
        params = (user_id,)
        self.db.execute_query(query, params)
