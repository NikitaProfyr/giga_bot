def get_chat_id_in_message(message: dict) -> int:
    """Функция возвращает id чата с пользователем исходя из события"""
    chat_id = 0
    if 'message' in message:
        chat_id = message['message']['chat']['id']
    if 'callback_query' in message:
        chat_id = message['callback_query']['message']['chat']['id']
    return int(chat_id)


def get_event_type(message: dict) -> str:
    """Функция возвращает тип события"""
    if 'callback_query' in message:
        return 'click_button'

    return 'unknown'
