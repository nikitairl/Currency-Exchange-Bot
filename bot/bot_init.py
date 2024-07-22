import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

default = DefaultBotProperties(
    parse_mode="HTML",
)
bot = Bot(token=os.getenv("BOT_API_TOKEN"), default=default)
dp = Dispatcher()
