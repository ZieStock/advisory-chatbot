from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import UserRoutes, AuthRouter, MessagesRouter, WatchListsRouter, ChatRouter
from exception import GlobalException
from database import Base, engine
from service import KafkaService
import asyncio
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
app.include_router(ChatRouter)
@app.on_event("startup")
async def startup_event():
    kafka_service = KafkaService(topic="signal") 
    asyncio.create_task(kafka_service.run())