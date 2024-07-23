import asyncio
import logging
import os
import xml.etree.ElementTree as ET

from aiohttp import ClientSession
from dotenv import load_dotenv

from db import REDIS_CLIENT

load_dotenv()

PARSE_URL = os.getenv("PARSE_URL")


async def fetch_exchange_rates():
    url = PARSE_URL
    logging.info(f"Fetching exchange rates from {url}")
    async with ClientSession() as session:
        async with session.get(url) as response:
            logging.info("Exchange rates fetched successfully")
            return await response.text()


def parse_exchange_rates(xml_data):
    logging.info("Parsing exchange rates")
    try:
        pre_text = ET.fromstring(xml_data)
        rates = {}
        for valute in pre_text.findall("Valute"):
            char_code = valute.find("CharCode").text
            value = valute.find("Value").text.replace(",", ".")
            nominal = valute.find("Nominal").text
            rates[char_code] = float(value) / float(nominal)
        logging.info("Exchange rates parsed successfully")
        return rates
    except ET.ParseError as e:
        logging.error(f"Error parsing XML data: {e}")
        return {}


async def update_redis_rates():
    logging.info("Updating Redis with new exchange rates")
    xml_data = await fetch_exchange_rates()
    rates = parse_exchange_rates(xml_data)
    for char_code, rate in rates.items():
        REDIS_CLIENT.set(char_code, rate)
    logging.info("Redis update completed")
    return


if __name__ == "__main__":
    asyncio.run(update_redis_rates())
