from pydantic import BaseModel
from enums import MessageRole

class MessagesRequest(BaseModel):
    user_id: int
    role: MessageRole
    content: str