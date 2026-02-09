from src.storage.db_manager import DBManager
from src.models.user import User
import logging

class UserRepository:
    def __init__(self):
        self.db = DBManager()

    def map_row_to_user(self, row) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            created_at=row["created_at"],
            inactive_at=row["inactive_at"],
            active=bool(row["active"])
        )

    def create_user(self, user: User):
        try:
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
            logging.debug(f"[USER-REPOSITORY] Created user: {user.email}")
            return user

        except Exception as error:
            logging.error(f"[USER-REPOSITORY] Fail to create user: {error}")
            raise error
    
    def get_all_users(self) -> list[User]:
        try:
            query = "SELECT id, name, email, created_at, inactive_at, active FROM users"
            result = self.db.execute_query(query)

            users_list = []
            if result:
                for row in result:
                    users_list.append(self.map_row_to_user(row))

            logging.debug(f"[USER-REPOSITORY] Returned {len(users_list)} users")
            return users_list

        except Exception as error:
            logging.error(f"[USER-REPOSITORY] Fail to get all users: {error}")
            raise error

    def get_user_by_id(self, user_id) -> User:
        try:
            query = "SELECT id, name, email, created_at, inactive_at, active FROM users WHERE id = ?"
            params = (user_id,)
            result = self.db.execute_query(query, params)

            if result:
                return self.map_row_to_user(result[0])

            logging.debug(f"[USER-REPOSITORY] User ID {user_id} not found")
            return None

        except Exception as error:
            logging.error(f"[USER-REPOSITORY] Fail to get user by ID: {error}")
            raise error

    def get_user_by_name(self, user_name) -> list[User]:
        try:
            query = "SELECT id, name, email, created_at, inactive_at, active FROM users WHERE name LIKE ?"
            params = (f"%{user_name}%",)
            result = self.db.execute_query(query, params)

            users_list = []
            if result:
                for row in result:
                    users_list.append(self.map_row_to_user(row))
            
            logging.debug(f"[USER-REPOSITORY] Found {len(users_list)} users with name like '{user_name}'")
            return users_list
            
        except Exception as error:
            logging.error(f"[USER-REPOSITORY] Fail to get user by name: {error}")
            raise error
    
    def get_user_by_email(self, user_email) -> User:
        try:
            query = "SELECT id, name, email, created_at, inactive_at, active FROM users WHERE email = ?"
            params = (user_email,)
            result = self.db.execute_query(query, params)

            if result:
                return self.map_row_to_user(result[0])

            logging.debug(f"[USER-REPOSITORY] Email {user_email} not found")
            return None

        except Exception as error:
            logging.error(f"[USER-REPOSITORY] Fail to get user by email: {error}")
            raise error
    
    def update_user(self, user: User):
        try:
            if user.active:
                user.inactive_at = None

            query = """
                UPDATE users SET name = ?, email = ?, active = ?, inactive_at = ? 
                WHERE id = ?
            """
            params = (
                user.name,
                user.email,
                user.active,
                user.inactive_at,
                user.id
            )

            self.db.execute_query(query, params)
            logging.debug(f"[USER-REPOSITORY] Updated user ID: {user.id}")

        except Exception as error:
            logging.error(f"[USER-REPOSITORY] Fail to update user: {error}")
            raise error

    def delete_user(self, user_id):
        try:
            query = """
                UPDATE users SET active = 0, inactive_at = datetime('now') 
                WHERE id = ?
            """
            params = (user_id,)
            self.db.execute_query(query, params)
            logging.debug(f"[USER-REPOSITORY] Soft deleted user ID: {user_id}")

        except Exception as error:
            logging.error(f"[USER-REPOSITORY] Fail to delete user: {error}")
            raise error