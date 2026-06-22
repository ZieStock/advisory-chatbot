from sqlalchemy.orm import Session
from entity import UserEntity
from exception import AppException, Errorcode
from core import decode_token, encode_token, verify_password
from dto.request import AuthRequest
from dto.response import AuthResponse

class AuthService:
    @staticmethod
    def login(db: Session, request: AuthRequest):
        user = db.query(UserEntity).filter(UserEntity.username == request.username).first()
        if user is None and not verify_password(request.password, UserEntity.password):
            raise AppException(Errorcode.LOGIN_FAILED)
        token = encode_token({
            "id": user.id,
            'name': user.username,
            'role': user.role.value,
            'email': user.email
        })
        return AuthResponse(token=token)