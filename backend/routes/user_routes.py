from service import UserService
from database import get_db
from fastapi import Depends, APIRouter
from dto.response import UserResponse
from dto.request.users import UserRequest, ChangePasswordRequest
from sqlalchemy.orm import session
from core import decode_token, require_role
router = APIRouter(prefix='/users')
@router.post("", response_model=UserResponse)
def createUser(request: UserRequest, db:session = Depends(get_db)):
    return UserService.create_user(db, request)
@router.put("/update")
def updateUser(request: UserRequest ,payload = Depends(decode_token), db:session = Depends(get_db)):
    return UserService.update_user(db, payload['id'], request)
@router.get("/me")
def getMe(payload = Depends(decode_token), db: session = Depends(get_db)):
    return UserService.get_me(db, payload['id'])
@router.put("/block/{user_id}")
def block_user(user_id: int, db: session = Depends(get_db), role = Depends(require_role(['Admin']))):
    return UserService.block_user(db, user_id)
@router.put('/change-password')
def change_password(request: ChangePasswordRequest, payload = Depends(decode_token), db: session = Depends(get_db)):
    return UserService.change_password(db, payload['id'], request)
@router.put('/soft-delete')
def soft_delete(payload = Depends(decode_token), db: session = Depends(get_db)):
    return UserService.soft_delete(db, payload['id'])
@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: session = Depends(get_db)):
    return UserService.delete_user(db, user_id)