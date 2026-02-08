from json import dumps

class User:
    def __init__(self, id, name, email, created_at=None, inactive_at=None, active=True):
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
            "created_at": str(self.created_at) if self.created_at else None,
            "inactive_at": str(self.inactive_at) if self.inactive_at else None,
            "active": self.active
        }
    
    def to_json(self):
        return dumps(self.to_dict())
