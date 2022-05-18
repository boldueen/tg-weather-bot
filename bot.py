# -*- coding: utf-8 -*-
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.handlers import basic_router
from tgbot.handlers import weather_router
from tgbot.logger import logger


async def main():
    logger.info("Starting Bot...")

    # config loader
    config = load_config(
        env_path='.env',
        ini_path='settings.ini',
    )

    # fsm storage
    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode=config.misc.parse_mode)
    dp = Dispatcher(storage=storage)

    for router in [
        basic_router,
        weather_router
    ]:
        dp.include_router(router)

    await dp.start_polling(bot, config=config)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error("Bot was stopped...")
