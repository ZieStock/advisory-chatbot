from fastapi import APIRouter,Depends
from sqlalchemy.orm import session
from service import AuthService
from database import get_db
from dto.request import AuthRequest
router = APIRouter(prefix='/auth')
@router.post('/login')
def login(request: AuthRequest,db: session = Depends(get_db)):
    return AuthService.login(db, request)