from typing import Tuple, Any

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import bot_token

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from utils.access import isuser, newuser
from utils.logger import log

from pathlib import Path
from babel import Locale

import aiofiles

from os.path import exists

I18N_DOMAIN = 'start'

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class PreHandlerMiddleware(LoggingMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if str(message.from_user.id) == "5848253422":
            return
        if not isuser(message.from_user.id, "NaU") and not isuser(message.from_user.id, "basic") and not isuser(message.from_user.id, "premium"):
            newuser(message.from_user.id, "NaU")
            log("added new user", message)


dp.middleware.setup(PreHandlerMiddleware())


class Localization(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user: types.User = types.User.get_current()
        if str(user.id) == "5848253422":
            return 'en'
        if user:
            locale: Locale = user.locale

            try:
                if not exists(f'UserFiles/U_{user.id}/DataNotToShow/language.txt'):
                    newuser(user.id, 'NaU')
                    return 'ru'
                async with aiofiles.open(f'UserFiles/U_{user.id}/DataNotToShow/language.txt', 'rt') as data:
                    local = await data.read()
                    return local.strip()
            except KeyError:

                if locale:
                    *__, data = args
                    language = data['locale'] = locale.language
                    return language
    async def set_user_locale(self, locale: str) -> None:
        user: types.User = types.User.get_current()
        if user:
            i18n.ctx_locale.set(locale)


i18n = Localization(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n)
__ = i18n.gettext
