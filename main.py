import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

from bot.middlewares import all_middleware
from utils.Conf import CF
from bot.handlers import dp


async def main() -> None:
    i18n = I18n(path="locales", default_locale="en", domain='messages')
    bot = Bot(token=CF.bot.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await all_middleware(dp, i18n)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())