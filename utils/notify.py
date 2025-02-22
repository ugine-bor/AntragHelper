import logging
from aiogram import Dispatcher

from data.config import admins


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        await dp.bot.send_message(chat_id=admin, text="Парсер Запущен")


async def on_shutdown_notify(dp: Dispatcher):
    for admin in admins:
        await dp.bot.send_message(chat_id=admin, text="Парсер Выключен")
