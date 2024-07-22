import asyncio
import os
import xml.etree.ElementTree as ET

from aiohttp import ClientSession
from dotenv import load_dotenv

from bot.db import REDIS_CLIENT

load_dotenv()

PARSE_URL = os.getenv("PARSE_URL")


async def fetch_exchange_rates():
    url = PARSE_URL
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


def parse_exchange_rates(xml_data):
    pre_text = ET.fromstring(xml_data)
    rates = {}
    for valute in pre_text.findall("Valute"):
        char_code = valute.find("CharCode").text
        value = valute.find("Value").text.replace(",", ".")
        nominal = valute.find("Nominal").text
        rates[char_code] = float(value) / float(nominal)
    return rates


async def update_redis_rates():
    xml_data = await fetch_exchange_rates()
    rates = parse_exchange_rates(xml_data)
    for char_code, rate in rates.items():
        REDIS_CLIENT.set(char_code, rate)


if __name__ == "__main__":
    asyncio.run(update_redis_rates())
