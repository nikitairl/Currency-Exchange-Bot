import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from bot.db import REDIS_CLIENT


load_dotenv()

REDIS_CLIENT = REDIS_CLIENT
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=["exchange"])
async def convert_currency(message: types.Message):
    try:
        _, from_currency, to_currency, amount = message.text.split()
        amount = float(amount)
        from_rate = float(REDIS_CLIENT.get(from_currency).decode("utf-8"))
        to_rate = float(REDIS_CLIENT.get(to_currency).decode("utf-8"))
        result = amount * from_rate / to_rate
        await message.reply(
            f"{amount} {from_currency} = {result:.2f} {to_currency}"
        )
    except Exception:
        await message.reply(
            "Неверная команда. Используйте формат: /exchange USD RUB 10"
        )


async def main():
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
