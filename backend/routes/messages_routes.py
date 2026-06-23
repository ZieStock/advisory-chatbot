from fastapi import APIRouter, Depends
from database import get_db
from core import decode_token, require_role
from service import MessagesService
from dto.request.messages import MessagesRequest, UpdateMessagesRequest
from sqlalchemy.orm import Session

router = APIRouter(prefix='/messages')
@router.post("")
def save_message(request: MessagesRequest, db: Session = Depends(get_db)):
    return MessagesService.save_message(db, request)
@router.get("/{message_id}")
def get_by_id(message_id: int, db: Session = Depends(get_db)):
    return MessagesService.get_by_id(db, message_id)
@router.put("/{messages_id}")
def update_messages(messages_id:int, request: UpdateMessagesRequest, db: Session = Depends(get_db)):
    return MessagesService.update_messages(db, messages_id, request)
@router.get("")
def get_messages_by_user(payload = Depends(decode_token) ,db: Session = Depends(get_db)):
    return MessagesService.get_messages_by_user(db, payload['id'])
@router.delete("/{messages_id}")
def delete_messages(messages_id: int ,db: Session = Depends(get_db), role = Depends(require_role(['Admin', 'ADMIN']))):
    return MessagesService.delete_messages(db, messages_id)