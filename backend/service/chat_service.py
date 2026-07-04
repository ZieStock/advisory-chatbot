from fastapi import WebSocket, WebSocketDisconnect
from chatbot.chatbot_service import ChatbotService
from typing import Dict, Any
from sqlalchemy.orm import Session
from util import get_logger
import asyncio

logger = get_logger(__name__)

class ChatService:
    def __init__(self):
        self.bot = ChatbotService()
        self.active: Dict[Any, WebSocket] = {}
        logger.info(f"CHAT SERVICE INIT ID = {id(self)}")
    async def connect(self, websocket: WebSocket, user_info: Dict[Any, str]):
        self.active[user_info['id']] = websocket
        logger.info(f"Kết nối thành công đến {user_info['name']}")
    async def disconnect(self, user_info: Dict[str, Any]):
        if user_info['id'] in self.active:
            del self.active[user_info['id']]
            logger.info(f"{user_info['name']} đã tắt kết nối")
    async def chat(self, db: Session, websocket: WebSocket, user_info: Dict[Any, str]):
        await self.connect(websocket, user_info)
        try:
            while True:
                messages = await websocket.receive_text()
                res = await asyncio.to_thread(self.bot.chat, messages, db, user_info)
                await websocket.send_text(res)
        except WebSocketDisconnect:
            logger.warning("Lỗi kết nối đến websocket")
            await self.disconnect(user_info)
        except Exception as e:
            logger.debug(f"Lỗi không xác định {e}")
            await self.disconnect(user_info)
    async def send_message_async(self, ws: Any, message: str) -> bool:
        try:
            await ws.send_text(message)
            return True
        except Exception as e:
            logger.debug(f"Ignore WS send error: {e}")
            return False
chat_service = ChatService()