from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import UserRoutes, AuthRouter, MessagesRouter, WatchListsRouter
from exception import GlobalException
from database import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI()
GlobalException(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods = ['*'],
    allow_credentials = True
)
app.include_router(UserRoutes)
app.include_router(AuthRouter)
app.include_router(MessagesRouter)
app.include_router(WatchListsRouter)