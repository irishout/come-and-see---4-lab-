import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.messages import router
from api_keys import *

# Bot token can be obtained via https://t.me/BotFathe

# All handlers should be attached to the Router (or Dispatcher)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(token=bot_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

