from load import dp, __
from aiogram.dispatcher.filters import Command
from aiogram import types
from json import load

from utils.access import reduce, isuser
from utils.logger import log

from handlers.users.getdataCSV import urlpost

from requests import ConnectTimeout

import csv


@dp.message_handler(Command("request"))
async def req(message: types.Message):
    log("user tries to send premium /request", message)
    if isuser(message.from_user.id, "premium"):
        with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json', 'r') as fin:
            email = load(fin)['email']

        await message.answer(__("Отправляю запрос."))
        try:
            await urlpost(message, mode=3)  # POST request; mode=3 - premium

            with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/files_id.csv', 'r+') as file:
                reader = csv.reader(file)
                rows = [next(reader)]

                file.seek(0)
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(rows)
                file.truncate()

            reduce(message.from_user.id, usertype="premium")
            log("user successfully sended premium /request", message)
        except ConnectTimeout:
            await message.answer(__("При отправке запроса произошла ошибка.\nПопробуйте снова нажать /request."))
        except ConnectionError:
            await message.answer(__("При отправке запроса произошла ошибка.\nПопробуйте снова нажать /request."))
        else:
            await message.answer(__('''Ваш запрос на обработку документов отправлен.
            Результат придет вам на почту {}.''').format(email))
    else:
        log("user failed send premium request (no permission) (/request)", message)
        await message.answer(__("Нет доступа. Купите через /payplus."))
