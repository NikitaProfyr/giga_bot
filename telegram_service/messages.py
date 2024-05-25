import json

from telegram_service.telegram_api import send_message, delete_message


async def remove_message(message: dict) -> None:
    """
    Данный метод удаляет сообщение.
    """
    data = {
        "chat_id": message["message"]["chat"]["id"],
        "message_id": message["message"]["message_id"],
    }

    await delete_message(data)


async def send_approve_keyboard(target_chat_id, message_id, from_channel) -> None:
    """Данный метод отправляет клавиатуру с подтверждением публикации."""
    keyboard_post = {
        "chat_id": target_chat_id,
        "text": "К кому вы хотите обратиться?",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "Обратиться к ИИ",
                        "callback_data": json.dumps(
                            {"succ": True, "mid": message_id, "cid": from_channel}
                        ),
                    }
                ],
                [
                    {
                        "text": "Обратиться к менеджеру",
                        "callback_data": json.dumps(
                            {"succ": False, "mid": message_id, "cid": from_channel}
                        ),
                    }
                ],
            ],
            "resize_keyboard": True,
        },
    }

    await send_message(keyboard_post)


async def send_message_user(chat_id: str, text: str):
    """Данный метод отправляет сообщение пользователя от лица бота"""

    data = {"chat_id": chat_id, "text": text}
    await send_message(data)
