from pydantic import BaseModel

class UpdateMessagesRequest(BaseModel):
    content: str