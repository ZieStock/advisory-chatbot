from fastapi import APIRouter, Depends
from database import get_db
from service import WatchListsService
from dto.request.watchlists import WatchlistsRequest
from sqlalchemy.orm import session
from core import decode_token

router = APIRouter(prefix='/watchlists')
@router.post("")
def createWatchLists(request: WatchlistsRequest, payload = Depends(decode_token), db: session = Depends(get_db)):
    return WatchListsService.createWatchLists(db, payload['id'], request)
@router.get("/{watchlists_id}")
def get_by_watchlists(watchlists_id:int, payload = Depends(decode_token), db: session = Depends(get_db)):
    return WatchListsService.get_by_watchlists(db, payload['id'], watchlists_id)
@router.get("")
def get_all_by_user(payload = Depends(decode_token), db: session = Depends(get_db)):
    return WatchListsService.get_all_by_user(db, payload['id'])
@router.put("/{watchlists_id}")
def updateWatchLists(watchlists_id: int, request: WatchlistsRequest, payload = Depends(decode_token), db: session = Depends(get_db)):
    return WatchListsService.updateWatchLists(db, payload['id'], request, watchlists_id)
@router.delete("/{watchlists_id}")
def deleteWatchLists(watchlists_id:int, payload = Depends(decode_token), db: session = Depends(get_db)):
    return WatchListsService.deleteWatchLists(db, payload['id'], watchlists_id)