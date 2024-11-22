import asyncio
import os
import json

from aiogram import Bot, Dispatcher

from handlers.query_handler import router as query_handler
from handlers.command_handler import router as command_router
from handlers.callback_handler import router as callback_handler
from handlers.message_handler import router as message_handler
from utils.database import Database

import logging

logging.basicConfig(level=logging.INFO)

with open(os.path.join("config", "config.json"), "r", encoding="utf-8") as settings_file:
    settings = json.load(settings_file)

bot = Bot(token=settings["token"])

async def main():
    dp = Dispatcher()
    db = Database()
    dp.include_router(query_handler)
    dp.include_router(callback_handler)
    dp.include_router(command_router)
    dp.include_router(message_handler)
    await db.init_db()

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass