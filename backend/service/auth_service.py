from sqlalchemy.orm import Session
from entity import UserEntity
from exception import AppException, Errorcode
from core import encode_token, verify_password, decode_refresh_token, RedisClient
from dto.request import AuthRequest
from dto.response import AuthResponse, ApiResponse
from datetime import timedelta
class AuthService:
    @staticmethod
    def login(db: Session, request: AuthRequest):
        user = db.query(UserEntity).filter(UserEntity.username == request.username).first()
        if user is None or not verify_password(request.password, user.password):
            raise AppException(Errorcode.LOGIN_FAILED)
        data = {
            "id": user.id,
            'name': user.username,
            'role': user.role.value,
            'email': user.email
        }
        access_token = encode_token(data, timedelta(minutes=10), "access")
        refresh_token = encode_token(data, timedelta(days=3), "refresh")
        RedisClient.set(f"refresh_token:{refresh_token}", str(user.id), 3 * 24 * 60 * 60)
        return AuthResponse(access_token=access_token, refresh_token=refresh_token)
    @staticmethod
    def refresh_token(token: str):
        check = RedisClient.get(f"refresh_token:{token}")
        if check is None:
            raise AppException(Errorcode.REFRESH_TOKEN_INVALID)
        payload = decode_refresh_token(token)
        data = {
            "id": payload["id"],
            'name': payload["name"],
            'role': payload["role"],
            'email': payload["email"]
        }
        access_token = encode_token(data, timedelta(minutes=10), "access")
        return AuthResponse(access_token=access_token, refresh_token=token)
    @staticmethod
    def logout(token: str):
        RedisClient.delete(f"refresh_token:{token}")
        return ApiResponse(code=200, message="Đăng xuất thành công")