from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

import redis.asyncio as redis

from model.db_user_services import check_status_chat
from model.model_settings import get_redis
from .events import (
    check_method,
    check_secret_key,
    on_start_bot,
    error_type_event,
    on_click_button,
    ask_the_bot,
)
from fastapi import Request, Depends

from .utils import get_event_type, get_chat_id_in_message

EVENTS = {
    "click_button": on_click_button,
    "unknown": error_type_event,
}
EVENTS_FOR_AI = {"ask_the_bot": 123}


async def handle_bot_events(
    request: Request, secret_key: str, redis: redis.Redis = Depends(get_redis)
):
    check_method(request=request)
    check_secret_key(secret_key=secret_key)
    message = await request.json()
    chat_id = get_chat_id_in_message(message=message)
    status_chat = await check_status_chat(chat_id=chat_id, redis=redis)
    try:
        if "message" in message:
            if "text" in message["message"] and message["message"]["text"] == "/start":
                await on_start_bot(message=message, redis=redis)
                status_chat = await check_status_chat(chat_id=chat_id, redis=redis)
        if status_chat is True:
            await ask_the_bot(message=message)
        else:
            await EVENTS[get_event_type(message=message)](message)
    except Exception:
        raise HTTP_404_NOT_FOUND

    return HTTP_200_OK
