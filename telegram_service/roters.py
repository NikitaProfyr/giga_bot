from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from model.db_user_services import created_user, set_status_chat
from model.model_settings import db_helper, get_redis
from model.user_schemas import UserCreateSchema
from telegram_service.events import check_secret_key
from telegram_service.handle_event import handle_bot_events
import redis.asyncio as redis

telegram_router = APIRouter(prefix="/handle_bot_events", tags=["Telegram Router"])
api_router = APIRouter(prefix="/api", tags=["API"])


@telegram_router.post('/{secret_key:str}/')
async def handle_bot_events_router(request: Request, secret_key: str, redis: redis.Redis = Depends(get_redis)):
    """Роутер для отслеживания событий в телеграм"""
    return await handle_bot_events(request=request, secret_key=secret_key, redis=redis)


@api_router.post('/registration/{secret_key:str}')
async def registration_user(
        secret_key: str,
        user_data: UserCreateSchema,
        db: AsyncSession = Depends(db_helper.scoped_session_dependency),
        redis: redis.Redis = Depends(get_redis)
):
    """Роутер для регистрации пользователей"""
    check_secret_key(secret_key=secret_key)
    data = await created_user(user_data=user_data, db=db)
    if data == 200:
        await set_status_chat(chat_id=user_data.tg_channel_id, status_chat=user_data.status_chat, redis=redis)
