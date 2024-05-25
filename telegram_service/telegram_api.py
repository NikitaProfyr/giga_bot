import httpx

from settings import TELEGRAM_API_URL


client = httpx.AsyncClient()


async def send_message(data):
    """Функция отправляет сообщение пользователю"""
    method = 'sendMessage'
    url = TELEGRAM_API_URL + method
    response = await client.post(url, json=data, timeout=10)

    return response


async def delete_message(data):
    """Функция удаляет сообщение в диалоге"""
    method = 'deleteMessage'
    url = TELEGRAM_API_URL + method
    response = await client.post(url, json=data, timeout=10)

    return response
