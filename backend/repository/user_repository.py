from sqlalchemy.orm import Session
from entity import UserEntity

class UserRepository:
    @staticmethod
    def createUser(db:Session, user: UserEntity):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(UserEntity).filter(UserEntity.id == user_id).first()
    @staticmethod
    def updateUser(db:Session, user: UserEntity):
        db.commit()
        db.refresh(user)
        return user
    @staticmethod
    def deleteUser(db:Session, user: UserEntity):
        db.delete(user)
        db.commit()
        return user