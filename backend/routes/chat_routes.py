from fastapi import APIRouter, Depends, WebSocket, Query
from service.chat_service import chat_service
from core import decode_token
from database import get_db
from typing import Optional

router = APIRouter(prefix="/ws", tags=["Chat"])

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = Query(None), db = Depends(get_db)):
    await websocket.accept()
    user = decode_token(token)
    if not user:
        await websocket.send_json({"Token không hợp lệ hoặc đã hết hạn"})
    await chat_service.chat(db, websocket, user)