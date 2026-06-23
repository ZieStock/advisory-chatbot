from pydantic import BaseModel
from enums import MessageRole

class MessagesResponse(BaseModel):
    user_id: int
    role: MessageRole
    content: str
    model_config = {
        'from_attributes': True
    }