import asyncio
import logging
import asyncio
import aiomisc

# from aiogram import Bot, Dispatcher, Router, types
# from aiogram.filters import Command
# from aiogram.types import Message
logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter
TOKEN = "5144631756:AAFsyaBy0NfhV17vlLSittkdVJMCkeej5H4"


async def main():
    for i in range(1000):
        logger.info(f"sleep iteration -> {i}")
        await asyncio.sleep(10)


with aiomisc.entrypoint() as loop:
    loop.run_until_complete(main())
