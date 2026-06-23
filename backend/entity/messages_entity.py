from .base_time import BaseTime
from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum, Text
from enums import MessageRole

class MessagesEntity(Base, BaseTime):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
