import json
import httpx
from fastapi import Request, Depends
import redis.asyncio as redis
import settings
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from model.db_user_services import delete_status_chat
from model.model_settings import get_redis
from model.user_schemas import UserCreateSchema
from sberai_service.sberai_settings import ai_client

from telegram_service.messages import (
    send_approve_keyboard,
    remove_message,
    send_message_user,
)


def check_secret_key(secret_key):
    """Функция проверяет серкетный ключ от TELEGRAM WEBHOOK."""
    if secret_key != settings.WEBHOOK_SECRET_KEY:
        raise HTTP_401_UNAUTHORIZED


def check_method(request: Request):
    """Функция проверяет тип запроса 'POST'"""
    if request.method != "POST":
        raise HTTP_404_NOT_FOUND


async def error_type_event(message: dict):
    print("событие не определено")
    return HTTP_404_NOT_FOUND


async def on_start_bot(message: dict, redis: redis.Redis = Depends(get_redis)):
    chat_id = message["message"]["chat"]["id"]
    message_id = message["message"]["message_id"]
    await delete_status_chat(chat_id=int(chat_id), redis=redis)
    await send_approve_keyboard(
        target_chat_id=chat_id, message_id=message_id, from_channel=chat_id
    )
    await remove_message(message=message)


async def on_click_button(message: dict):
    chat_id = message["callback_query"]["message"]["chat"]["id"]
    user_id = int(message["callback_query"]["from"]["id"])
    user_name = message["callback_query"]["from"]["username"]
    complete_operation = json.loads(message["callback_query"]["data"])
    status_chat = ""
    if complete_operation["succ"]:
        status_chat = "With AI"
        text = "Задавайте ваш вопрос!"
        await send_message_user(chat_id=chat_id, text=text)
    else:
        status_chat = "With Assistent"
        await send_message_user(
            chat_id=chat_id,
            text="Обратиться к менеджеру вы сможете в следующих версиях )",
        )
    async with httpx.AsyncClient() as client:
        url = settings.API_URL + "/api/registration/" + settings.WEBHOOK_SECRET_KEY
        user_data = UserCreateSchema(
            id=user_id,
            user_name=user_name,
            tg_channel_id=chat_id,
            status_chat=status_chat,
        )

        data = await client.post(url=url, data=user_data.json(), timeout=10)
    await remove_message(message=message)


async def ask_the_bot(message: dict):
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]
    answer = await ai_client.ask_a_question(text=text)
    await send_message_user(chat_id=chat_id, text=answer)
