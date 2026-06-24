from chatbot.build_agent import BuildAgent
from chatbot.model import get_llm
from chatbot.system_prompt import SystemPrompt
from typing import Dict, Any
from sqlalchemy.orm import Session
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from service import MessagesService
from dto.request.messages import MessagesRequest
from util import get_logger

logger = get_logger(__name__)

class ChatbotService:
    def __init__(self):
        self.agent = BuildAgent(get_llm())
    def chat(self, messages: str, db: Session, user_info: Dict[str, Any], bot_name: str = 'chatbot chứng khoản'):
        thread_id = str(user_info.get("id", "0"))
        system_prompt = SystemPrompt(bot_name)
        histories = MessagesService.get_messages_by_user(db, thread_id)
        message = [SystemMessage(system_prompt)]
        for item in histories:
            if item.role == 'user':
                message.append(HumanMessage(item.content))
            else:
                message.append(AIMessage(item.content))
        message.append(HumanMessage(content=messages))
        try:
            result = self.agent.invoke({
                "messages": message
            })
            answer = result["messages"][-1].content
            MessagesService.save_message(db, MessagesRequest(user_id=thread_id,role="user", content=messages))
            MessagesService.save_message(db, MessagesRequest(user_id=thread_id, role="assistant", content=answer))
            return answer
        except Exception as e:
            logger.error(f"Lỗi từ chatbot {e}")
            raise e