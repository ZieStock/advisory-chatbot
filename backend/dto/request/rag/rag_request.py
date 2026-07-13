from pydantic import BaseModel

class RAGSearchRequest(BaseModel):
    text: str
    symbol: str
    k: int