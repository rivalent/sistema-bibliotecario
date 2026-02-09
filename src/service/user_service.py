from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.schemas.user_schema import UserRequest
from ulid import ULID
import datetime
import logging
import traceback

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create(self, name: str, email: str):
        try:
            user_id = str(ULID())
            created_at = datetime.datetime.now()
            
            name = name.strip()
            email = email.strip().lower()

            new_user = User(
                id=user_id,
                name=name,
                email=email,
                created_at=created_at,
                active=True,
                inactive_at=None
            )

            self.repo.create_user(new_user)

            logging.debug(f"[USER-SERVICE] Created: {new_user.email} (ID: {user_id})")
            return new_user

        except Exception as error:
            logging.error(f"[USER-SERVICE] Fail to create: {error} -> {traceback.format_exc()}")
            return None

    def list_all(self):
        try:
            list_users = self.repo.get_all_users()
            logging.debug(f"[USER-SERVICE] Found {len(list_users)} users")
            return list_users
        except Exception as error:
           logging.error(f"[USER-SERVICE] Fail to list: {error} -> {traceback.format_exc()}")
           return []

    def find_by_id(self, user_id: str):
        try:
            user_id = user_id.strip()
            user = self.repo.get_user_by_id(user_id)
            
            if not user:
                logging.info(f"[USER-SERVICE] User {user_id} not found")
                return None
            
            logging.debug(f"[USER-SERVICE] Found: {user.email}")
            return user

        except Exception as error:
            logging.error(f"[USER-SERVICE] Fail to find: {error} -> {traceback.format_exc()}")
            return None
    
    def activate(self, user_id: str):
        try:
            user_id = user_id.strip()
            
            user = self.find_by_id(user_id)
            if not user:
                return False

            user.active = True
            self.repo.update_user(user)
            
            logging.debug(f"[USER-SERVICE] Activated USER ID: {user_id}")
            return True

        except Exception as error:
            logging.error(f"[USER-SERVICE] Fail to activate: {error} -> {traceback.format_exc()}")
            return False

    def update(self, user_id: str, update_data: UserRequest): 
        try:
            user_id = user_id.strip()
            
            user = self.find_by_id(user_id)
            if not user:
                logging.warning(f"[USER-SERVICE] Attempt to update non-existent user: {user_id}")
                return None

            if update_data.name is not None:
                user.name = update_data.name.strip()
                
            if update_data.email is not None:
                user.email = update_data.email.strip().lower()

            self.repo.update_user(user)

            logging.debug(f"[USER-SERVICE] Updated: {user.name}")
            return user

        except Exception as error:
            logging.error(f"[USER-SERVICE] Fail to update: {error} -> {traceback.format_exc()}")
            return None

    def delete(self, user_id: str):
        try:
            user_id = user_id.strip()
            
            if not self.find_by_id(user_id):
                return False

            self.repo.delete_user(user_id)

            logging.debug(f"[USER-SERVICE] Soft Deleted USER ID: {user_id}")
            return True

        except Exception as error:
            logging.error(f"[USER-SERVICE] Fail to delete: {error} -> {traceback.format_exc()}")
            return False
