import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from bot_init import bot, dp
from db import REDIS_CLIENT
from parser import update_redis_rates
from handlers.user_handlers import user_router


PATH = os.path.dirname(__file__)

load_dotenv()

REDIS_CLIENT = REDIS_CLIENT
API_TOKEN = os.getenv("BOT_API_TOKEN")


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=PATH + "/logs/bot.log",
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
dp.include_router(user_router)


async def main():
    logger.info("Bot starting...")
    await update_redis_rates()
    scheduler = AsyncIOScheduler(
        gconfig={"apscheduler.timezone": "Europe/Moscow"}
    )
    scheduler.add_job(
        update_redis_rates, "cron", hour="20"
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    logger.info("Bot started!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
