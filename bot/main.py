import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from db import REDIS_CLIENT

PATH = os.path.dirname(__file__)

load_dotenv()

REDIS_CLIENT = REDIS_CLIENT
API_TOKEN = os.getenv("BOT_API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=PATH + "/logs/bot.log",
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@dp.message_handler(commands=["rates"])
async def send_exchange_rates(message: types.Message):
    rates = ""
    keys = REDIS_CLIENT.keys()
    for key in keys:
        rate = REDIS_CLIENT.get(key).decode("utf-8")
        rates += f"{key}: {rate}\n"
    await message.reply(rates)


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
    logger.info("Bot starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(Bot)
    logger.info("Bot started!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
