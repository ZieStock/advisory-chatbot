from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util import load_setting

engine = create_engine(load_setting.DATABASE)
SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()