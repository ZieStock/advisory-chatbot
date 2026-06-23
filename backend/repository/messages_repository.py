from sqlalchemy.orm import Session
from entity import MessagesEntity

class MessagesRepository:
    @staticmethod
    def saveMessage(db: Session, messages: MessagesEntity):
        db.add(messages)
        db.commit()
        db.refresh(messages)
        return messages
    @staticmethod
    def get_by_id(db: Session, messages_id: int):
        return db.query(MessagesEntity).filter(MessagesEntity.id == messages_id).first()
    @staticmethod
    def updateMessages(db: Session, messages: MessagesEntity):
        db.commit()
        db.refresh(messages)
        return messages
    @staticmethod
    def getMessages(db: Session, user_id: str, limit: int):
        return (
            db.query(MessagesEntity)
            .filter(MessagesEntity.user_id == user_id)
            .order_by(MessagesEntity.created_at.desc())
            .limit(limit)
            .all()
        )[::-1]
    @staticmethod
    def deleteMessages(db: Session, message: MessagesEntity):
        db.delete(message)
        db.commit()
        return message