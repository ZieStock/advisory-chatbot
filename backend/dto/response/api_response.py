from pydantic import BaseModel

class ApiResponse(BaseModel):
    code: int
    message: str
    model_config = {
        'from_attributes': True
    }