from typing import Optional
from datetime import datetime
import json

class User:
    def __init__(
        self,
        name: str, 
        email: str, 
        id: Optional[str] = None,
        created_at: Optional[datetime] = None, 
        inactive_at: Optional[datetime] = None, 
        active: bool = True
    ):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at
        self.inactive_at = inactive_at
        self.active = active
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at if self.created_at else None,
            "inactive_at": self.inactive_at if self.inactive_at else None,
            "active": self.active
        }

    def to_json(self):
        return json.dumps(self.to_dict())