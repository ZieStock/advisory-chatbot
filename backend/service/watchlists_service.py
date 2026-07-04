from entity import WatchListEntity
from sqlalchemy.orm import Session
from repository import WatchListsRepository
from dto.request.watchlists import WatchlistsRequest
from dto.response import WatchListsResponse

class WatchListsService:
    @staticmethod
    def createWatchLists(db: Session, user_id: int, request: WatchlistsRequest):
        Watchlists = WatchListEntity(
            user_id = user_id,
            symbol = request.symbol
        )
        return WatchListsResponse.model_validate(WatchListsRepository.createWatchLists(db, Watchlists))
    @staticmethod
    def get_by_watchlists(db: Session, user_id: int, watchlists_id: int):
        return WatchListsRepository.get_by_watchlists(db, user_id, watchlists_id)
    @staticmethod
    def get_by_symbol(db: Session, symbol: str):
        return WatchListsRepository.get_by_symbol(db, symbol)
    @staticmethod
    def get_all_by_user(db: Session, user_id: int):
        Watchlists = WatchListsRepository.get_all_by_user(db, user_id)
        return [WatchListsResponse.model_validate(watchlists) for watchlists in Watchlists]
    @staticmethod
    def updateWatchLists(db: Session, user_id: int, request: WatchlistsRequest, watchlists_id: int):
        Watchlists = WatchListsService.get_by_watchlists(db, user_id, watchlists_id)
        Watchlists.symbol = request.symbol
        return WatchListsResponse.model_validate(WatchListsRepository.updateWatchLists(db, Watchlists))
    @staticmethod
    def deleteWatchLists(db: Session, user_id: int, watchlists_id: int):
        Watchlists = WatchListsService.get_by_watchlists(db, user_id, watchlists_id)
        return WatchListsResponse.model_validate(WatchListsRepository.deleteWatchLists(db, Watchlists))
