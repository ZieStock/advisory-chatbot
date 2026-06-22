from database import Base
from sqlalchemy import Column, Enum, String, Integer, Boolean
from enums import UserStatus, UserRole
class UserEntity(Base):
    __tablename__ = 'users'
    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), nullable=False)
    is_deleted = Column(Boolean, default=False)