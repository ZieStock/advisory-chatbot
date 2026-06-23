from pydantic import BaseModel

class WatchListsResponse(BaseModel):
    user_id: int
    symbol: str
    model_config = {
        'from_attributes': True
    }