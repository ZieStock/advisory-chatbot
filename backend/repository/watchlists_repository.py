from entity import WatchListEntity
from sqlalchemy.orm import Session

class WatchListsRepository:
    @staticmethod
    def createWatchLists(db: Session, WatchLists: WatchListEntity):
        db.add(WatchLists)
        db.commit()
        db.refresh(WatchLists)
        return WatchLists
    @staticmethod
    def updateWatchLists(db: Session, WatchLists: WatchListEntity):
        db.commit()
        db.refresh(WatchLists)
        return WatchLists
    @staticmethod
    def get_by_watchlists(db: Session, user_id: int, watchlists_id):
        return db.query(WatchListEntity).filter(WatchListEntity.id  == watchlists_id, WatchListEntity.user_id == user_id).first()
    @staticmethod
    def get_all_by_user(db: Session, user_id: int):
        return db.query(WatchListEntity).filter(WatchListEntity.user_id == user_id).all()
    @staticmethod
    def deleteWatchLists(db:Session, WatchLists: WatchListEntity):
        db.delete(WatchLists)
        db.commit()
        return WatchLists