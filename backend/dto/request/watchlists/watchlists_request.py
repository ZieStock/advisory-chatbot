from pydantic import BaseModel

class WatchlistsRequest(BaseModel):
    symbol: str