from pydantic import BaseModel
from enums import UserStatus, UserRole
class UserResponse(BaseModel):
    username: str
    email: str
    status: UserStatus
    role: UserRole
    model_config = {
        'from_attributes': True
    }