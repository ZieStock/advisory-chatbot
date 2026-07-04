from core import KafkaClient
from util import get_logger
from service import WatchListsService
from service.chat_service import chat_service
from database import SessionLocal
import asyncio

logger = get_logger(__name__)

class KafkaService:
    def __init__(self, topic):
        kafka = KafkaClient("config/consumer.yaml")
        self.consumer = kafka.kafka_consumer(topic)
        self.msg = self.consume_messages()
    def consume_messages(self):
        for msg in self.consumer:
            if msg and msg.value:
                yield msg.value
    async def run(self):
        while True:
            try:
                signal = await asyncio.to_thread(next, self.msg)
                logger.info(signal)
                if not signal:
                    continue
                symbol = signal.get("symbol")
                action = signal.get("action")
                price = signal.get("price")
                db = SessionLocal()
                try:
                    subscribers = WatchListsService.get_by_symbol(db, symbol)
                    logger.info(f"Danh sách người đăng ký: {[f'user_id={u.user_id}, symbol={u.symbol}' for u in subscribers]}")
                    if not subscribers:
                        logger.info("Không có người đăng ký theo dõi mã này")
                        continue
                    for user in subscribers:
                        message_content = f"**Tín hiệu**: Mã **{symbol}** đã kích hoạt vùng giá {price}. Khuyến nghị: {action}"
                        ws = chat_service.active.get(user.user_id)
                        await chat_service.send_message_async(ws, message_content)
                        logger.info(f"Đã gửi tín hiệu trực tiếp cho User {user.user_id}")
                except Exception as e:
                    logger.error(f"Lỗi xử lý: {e}", exc_info=True)
                finally:
                    db.close()
            except Exception as e:
                logger.error(f"Error: {e}", exc_info=True)
