import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

from db import REDIS_CLIENT

load_dotenv()


user_router = Router()


@user_router.message(Command(commands=["start"]))
async def start(message: Message):
    buttons = [
        [KeyboardButton(text="/rates")],
        [KeyboardButton(text="/exchange_guide")],
    ]
    keyboard = ReplyKeyboardMarkup(
        is_persistent=True, keyboard=buttons, resize_keyboard=True
    )
    await message.answer(
        "Welcome! Use the buttons below to get started.\n"
        "This bot can show you current exchange rates.\n"
        "Exchange rates updated every 20:00.\n",
        reply_markup=keyboard,
    )


@user_router.message(Command(commands=["exchange_guide"]))
async def send_guide(message: Message):
    await message.answer(
        "To exchange currency, use: \n/exchange FROM TO AMOUNT"
    )


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
        await message.reply(
            f"Converting {amount} {from_currency} -> {to_currency}."
        )
        amount = float(amount)
        from_rate = float(REDIS_CLIENT.get(from_currency))
        to_rate = float(REDIS_CLIENT.get(to_currency))
        result = amount * from_rate / to_rate
        await message.answer(
            f"{amount} {from_currency} = {result:.2f} {to_currency}"
        )
    except Exception:
        logging.exception("Failed to convert currency")
        await message.answer(
            "Wrong format or unknown currency. Example: /exchange USD BYN 10"
        )
