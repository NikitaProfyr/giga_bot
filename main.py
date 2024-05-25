
from fastapi import FastAPI


import httpx

from sberai_service.sberai_settings import ai_client
from telegram_service.roters import telegram_router, api_router
from telegram_service.tg_webhook import set_webhook, remove_webhook

client = httpx.AsyncClient()
app = FastAPI(
    title="TZ App",
    description="created by Nikita Profir",
)
app.include_router(router=telegram_router)
app.include_router(router=api_router)


@app.on_event("startup")
async def startup_event():
    await set_webhook()
    await ai_client.authorization()


@app.on_event("shutdown")
async def shutdown_event():
    await remove_webhook()
