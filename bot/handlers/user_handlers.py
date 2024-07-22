from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from db import REDIS_CLIENT

load_dotenv()


user_router = Router()


@user_router.message(Command(commands=["rates"]))
async def send_exchange_rates(message: Message):
    rates = ""
    keys = REDIS_CLIENT.keys()
    for key in keys:
        rate = REDIS_CLIENT.get(key)
        rates += f"{key}: {rate}\n"
    await message.reply(rates)


@user_router.message(Command(commands=["exchange"]))
async def convert_currency(message: Message):
    try:
        _, from_currency, to_currency, amount = message.text.split()
        amount = float(amount)
        from_rate = float(REDIS_CLIENT.get(from_currency))
        to_rate = float(REDIS_CLIENT.get(to_currency))
        result = amount * from_rate / to_rate
        await message.reply(
            f"{amount} {from_currency} = {result:.2f} {to_currency}"
        )
    except Exception:
        await message.reply(
            "Неверная команда. Используйте формат: /exchange USD RUB 10"
        )
