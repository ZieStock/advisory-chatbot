from sqlalchemy.orm import Session
from dto.request.messages import MessagesRequest, UpdateMessagesRequest
from dto.response import MessagesResponse
from repository import MessagesRepository
from entity import MessagesEntity
from exception import AppException, Errorcode

class MessagesService:
    @staticmethod
    def save_message(db: Session, request: MessagesRequest):
        messages = MessagesEntity(
            user_id=request.user_id,
            role=request.role,
            content=request.content
        )
        return MessagesResponse.model_validate(MessagesRepository.saveMessage(db, messages))
    @staticmethod
    def get_by_id(db: Session, messages_id: int):
        message = MessagesRepository.get_by_id(db, messages_id)
        if message is None:
            raise AppException(Errorcode.MESSAGE_NOT_FOUND)
        return message
    @staticmethod
    def update_messages(db: Session, messages_id: int, request: UpdateMessagesRequest):
        message = MessagesService.get_by_id(db, messages_id)
        message.content = request.content
        return MessagesResponse.model_validate(MessagesRepository.updateMessages(db, message))
    @staticmethod
    def get_messages_by_user(db: Session, user_id: str, limit: int = 10):
        messages = MessagesRepository.getMessages(db, user_id, limit)
        return [MessagesResponse.model_validate(m) for m in messages]
    @staticmethod
    def delete_messages(db: Session, messages_id: int):
        message = MessagesService.get_by_id(db, messages_id)
        return MessagesResponse.model_validate(MessagesRepository.deleteMessages(db, message))