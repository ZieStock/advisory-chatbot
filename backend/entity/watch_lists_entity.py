from sqlalchemy import Column, Enum, Integer, ForeignKey
from util import SYMBOLS
from database import Base
from .base_time import BaseTime

class WatchListEntity(Base, BaseTime):
    __tablename__ = "WatchLists"
    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(Enum(*SYMBOLS, name="symbol_enum"), nullable=False)