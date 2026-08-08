from redis import Redis, RedisError
from util import load_setting, get_logger

logger = get_logger(__name__)

class RedisClient:
    client = Redis(host=load_setting.REDIS_HOST, port=load_setting.REDIS_PORT, password=load_setting.REDIS_PASSWORD)
    @classmethod
    def set(cls, key: str, value: str, expire: int):
        try:
            cls.client.set(key, value, expire)
        except RedisError as e:
            logger.error(f"Lỗi lưu Redis: {e}")
    @classmethod
    def get(cls, key: str):
        try:
            return cls.client.get(key)
        except RedisError as e:
            logger.error(f"Lỗi lấy Redis: {e}")
            return None
    @classmethod
    def delete(cls, key: str):
        try:
            cls.client.delete(key)
        except RedisError as e:
            logger.error(f"Lỗi xóa Redis: {e}")