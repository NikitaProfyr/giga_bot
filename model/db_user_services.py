from fastapi import Depends
from sqlalchemy import select, and_

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from model.model_settings import get_redis
from model.user_models import User
from model.user_schemas import UserSchema

import redis.asyncio as redis


async def created_user(user_data: UserSchema, db: AsyncSession):
    """Функция добавляет пользователя в бд"""
    user = await db.scalar(select(User).where(and_(User.id == user_data.id)))
    if user:
        user.user_name = user_data.user_name
    else:
        user = User(
            id=int(user_data.id),
            user_name=user_data.user_name,
            tg_channel_id=user_data.tg_channel_id,
        )
    db.add(user)
    await db.commit()
    return HTTP_200_OK


async def set_status_chat(
    chat_id: int, status_chat: str, redis: redis.Redis = Depends(get_redis)
):
    """Функция устанавливает статус чата в редис"""
    await redis.set(chat_id, status_chat)


async def delete_status_chat(chat_id: int, redis: redis.Redis = Depends(get_redis)):
    """Функция удаляет статус чата в редис"""
    await redis.delete(chat_id)


async def check_status_chat(
    chat_id: int, redis: redis.Redis = Depends(get_redis)
) -> bool | None:
    """Функция проверяет статус чата, если статус"""
    status_chat = await redis.get(chat_id)
    if status_chat == "With AI":
        return True
    if status_chat == "With Assistent":
        return False
    return None
