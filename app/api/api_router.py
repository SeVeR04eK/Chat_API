from fastapi import APIRouter

from app.api.http import *
from app.api.websockets import chat_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(room_router)
api_router.include_router(chat_router)
api_router.include_router(history_router)

