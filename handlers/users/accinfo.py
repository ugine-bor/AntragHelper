from load import dp, __
from utils.access import accessnum
from utils.logger import log

from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types import ParseMode
import aiogram.utils.markdown as md

from os.path import exists, isfile
from os import listdir

import json


@dp.message_handler(Command("info"))
async def information(message: types.Message):
    log("user looks /info", message)
    if exists(f"UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json"):
        with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json', 'r') as fin:
            email = json.load(fin)['email']
    else:
        email = __('Неизвестно')
    if exists(f'UserFiles/U_{message.from_user.id}/DataNotToShow/language.txt'):
        with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/language.txt', 'rt') as data:
            local = data.read().strip()
    else:
        local = __("Неизвестно")
    filenum = len([name for name in listdir(f"UserFiles/U_{message.from_user.id}/DataVisible") if isfile(name)])
    await message.answer(md.text(__('''
Информация об аккаунте {} {}:
{} {}

{} {}

{} {}

{} {}

{}
  Basic - {}
  Premium - {}
  
Подробнее о возможностях аккаунтов Basic и Premium смотрите в /help
''').format(
        message.from_user.first_name if message.from_user.last_name else '',
        message.from_user.last_name if message.from_user.last_name else '',
        md.italic('id:'), md.italic(message.from_user.id),
        md.bold(__('Язык:')), local,
        md.bold('email:'), email,
        md.bold(__('Количество загруженных файлов:')),
        filenum,
        md.bold(__('Количеств доступов к командам:')),
        accessnum(message.from_user.id, "basic"),
        accessnum(message.from_user.id, "premium")
    )), parse_mode=ParseMode.MARKDOWN)
