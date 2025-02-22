from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode
import aiogram.utils.markdown as md

from load import dp, __
from utils.access import adder, isuser, newuser
from utils.logger import log

import requests

from states.getstate import Getmail as getmailstate

from os.path import exists

from csv import writer

mailstate = getmailstate()


@dp.message_handler(Command("send"))
async def urlpost(message: types.Message):
    print("started")
    await message.answer("started")
    url = "https://145.249.247.109:8443/BotAntragTest/hs/bots/Post"  # "https://httpbin.org/anything" "https://145.249.247.109:8443/BotAntragTest/hs/bots/Post"
    data = {'chat': 'what_is_chat'}
    req = requests.post(url, json=data, verify=False)
    print(req.status_code, "-------------", req.text, sep='\n')
    await message.answer("done")


@dp.message_handler(Command("help"))
async def helper(message: types.Message):
    log("used /help command", message)
    await message.answer(md.text(__('''
{}
/help - Показывает это сообщение.
/basic - Переход к базовым функциям сайта.
/plus - Переход к премиум функциям.
/info - Получить информацию об аккаунте.
/lang - Изменить язык бота.
/webapp - Наш сайт внутри телеграма.
/end - Прекратить выполнение (почти) любого действия.

{}
/send - Проверка отправки POST запроса
/mail - Изменить email
''').format(
        md.bold(__('Общие команды:')),
        md.bold(__('Секретные админские команды:'))
    )), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(Command("webapp"))
async def webapp(message: types.Message):
    log("used /webapp command", message)
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("ТЕСТ", web_app=WebAppInfo(url="https://alexsoft.kz:8443/hab/")))
    await message.answer(__("Открытие страницы сайта внутри телеграма."), reply_markup=markup)


@dp.message_handler(Command("mail"))
async def mailchange(message: types.Message):
    await message.answer(__("Чтобы продолжить необходимо ввести email"))

    await mailstate.getmail.set()


@dp.message_handler(Command("hack"))
async def becomeuser(message: types.Message):
        # Basic
    if isuser(message.from_user.id, usertype="basic", nul=True):
        adder(message.from_user.id, "basic", 1)
        await message.reply('+1 доступ к командам basic')
    elif not isuser(message.from_user.id, usertype="basic", nul=True):
        newuser(message.from_user.id, usertype="basic", howmuch=1)
        await message.reply('добавлен в usersbasic')
    # Premium
    if isuser(message.from_user.id, usertype="premium", nul=True):
        adder(message.from_user.id, usertype="premium", howmuch=1)
        if not exists(f"UserFiles/U_{message.from_user.id}/DataNotToShow/files_id.csv"):
            with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/files_id.csv', 'wt', encoding='utf-8',
                      newline='') as file:
                csv_writer = writer(file)
                csv_writer.writerow(('filename', 'fileid'))
        await message.reply('+1 доступ к командам premium')
    elif not isuser(message.from_user.id, usertype="premium", nul=True):
        newuser(message.from_user.id, usertype="premium", howmuch=1)

        await message.reply('добавлен в userspremium')
    if not exists(f"UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json"):
        await message.reply('Не указана почта. Используйте /mail')


@dp.message_handler(state='*', commands='end')
@dp.message_handler(Text(equals='end', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    log("used /end command", message)
    # Allow user to cancel any action
    current_state = await state.get_state()
    if current_state is None:
        return
    elif __import__("handlers").users.getpayment.userstate._group_name != current_state.split(':')[0]:
        log(f"finished state {current_state.split(':')[0]}", message)
        await state.finish()
        await message.reply(__('Действие завершено.'), reply_markup=types.ReplyKeyboardRemove())
    else:
        log(f"tried to finish {current_state.split(':')[0]} state, but failed", message)
        await message.answer(__("Нельзя завершить данное действие."))
