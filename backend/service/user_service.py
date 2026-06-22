from sqlalchemy.orm import session
from entity import UserEntity
from repository import UserRepository
from dto.request.users import UserRequest, ChangePasswordRequest
from dto.response import UserResponse
from enums import UserStatus, UserRole
from exception import AppException, Errorcode
from core import hash_password, verify_password
class UserService:
    @staticmethod
    def create_user(db: session, request: UserRequest):
        user = UserEntity(
            username = request.username,
            password = hash_password(request.password),
            email = request.email,
            role = UserRole.USER,
            status = UserStatus.ACTIVE
        )
        return UserResponse.model_validate(UserRepository.createUser(db, user))
    @staticmethod
    def get_by_id(db: session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)
        if user is None:
            raise AppException(Errorcode.USER_NOT_FOUND)
        return user
    @staticmethod
    def update_user(db:session, user_id:int, request: UserRequest):
        user = UserService.get_by_id(db, user_id)
        if user.status == UserStatus.BLOCKED:
            raise AppException(Errorcode.USER_BLOCKED)
        user.username = request.username
        user.password = hash_password(request.password)
        user.email = request.email
        return UserResponse.model_validate(UserRepository.updateUser(db, user))
    @staticmethod
    def get_me(db: session, user_id):
        return UserResponse.model_validate(UserRepository.get_by_id(db, user_id))
    @staticmethod
    def block_user(db: session, user_id: int):
        user = UserService.get_by_id(db, user_id)
        if user.status == UserStatus.BLOCKED:
            raise AppException(Errorcode.USER_ALREADY_BLOCKED)
        user.status = UserStatus.BLOCKED
        return UserResponse.model_validate(UserRepository.updateUser(db, user))
    @staticmethod
    def change_password(db: session, user_id: int, request: ChangePasswordRequest):
        user = UserService.get_by_id(db, user_id)
        if not verify_password(request.old_password, user.password):
            raise AppException(Errorcode.INVALID_PASSWORD)
        if user.status == UserStatus.BLOCKED:
            raise AppException(Errorcode.USER_BLOCKED)
        if user.is_deleted == True:
            raise AppException(Errorcode.USER_NOT_FOUND)
        user.password = hash_password(request.new_password)
        return UserResponse.model_validate(UserRepository.updateUser(db, user))
    @staticmethod
    def soft_delete(db:session, user_id: int):
        user = UserService.get_by_id(db, user_id)
        user.is_deleted = True
        return UserResponse.model_validate(UserRepository.updateUser(db, user))
    @staticmethod
    def delete_user(db: session, user_id: int):
        user = UserService.get_by_id(db, user_id)
        return UserResponse.model_validate(UserRepository.deleteUser(db, user))