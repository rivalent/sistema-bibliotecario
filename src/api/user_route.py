import logging
import traceback
from fastapi import APIRouter, HTTPException, status
from src.service.user_service import UserService
from src.schemas.user_schema import UserRequest, UserUpdate

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
service = UserService()

@router.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserRequest):
    try:
        new_user = service.create(
            name=user_data.name,
            email=user_data.email
        )

        if not new_user:
            raise HTTPException(status_code=400, detail="Failed to create user.")

        logging.debug(f"[USER-API] Created successfully: {new_user.id}")
        return new_user.to_dict()

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[USER-API] Fail to create: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/users', status_code=status.HTTP_200_OK)
def list_users():
    try:
        users = service.list_all()

        logging.debug(f"[USER-API] List all: {len(users)} users found")
        return [user.to_dict() for user in users]

    except Exception as error:
        logging.error(f"[USER-API] Fail to list: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/users/{user_id}', status_code=status.HTTP_200_OK)
def get_by_id(user_id: str):
    try:
        user = service.find_by_id(user_id)

        if not user:
            logging.debug(f"[USER-API] User {user_id} not found (404)")
            raise HTTPException(status_code=404, detail="User not found")
        
        logging.debug(f"[USER-API] Found user: {user.name} | {user.email}")
        return user.to_dict()

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[USER-API] Fail to find: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.patch('/users/{user_id}/activate', status_code=status.HTTP_200_OK)
def activate_user(user_id: str):
    try:
        success = service.activate(user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="User not found or failed to activate")
        
        return {"message": "User activated successfully"}

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[USER-API] Fail to activate: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.put('/users/{user_id}', status_code=status.HTTP_200_OK)
def update_user(user_id: str, user_data: UserUpdate):
    try:
        updated_user = service.update(
            user_id, 
            user_data
        )

        if not updated_user:
            logging.debug(f"[USER-API] Update failed: User {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        logging.debug(f"[USER-API] Updated successfully: {updated_user.id}")
        return updated_user.to_dict()

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[USER-API] Fail to update: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))

@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    try:
        success = service.delete(user_id)

        if not success:
            logging.debug(f"[USER-API] Delete failed: User {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")

        logging.debug(f"[USER-API] Deleted successfully: {user_id}")
        return 

    except Exception as error:
        if isinstance(error, HTTPException): raise error
        logging.error(f"[USER-API] Fail to delete: {error} -> {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(error))
