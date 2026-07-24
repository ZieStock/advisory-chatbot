from pydantic import BaseModel

class SymbolsRequest(BaseModel):
    symbols: list[str]