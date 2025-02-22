from load import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from states.getstate import GetDataState as gt
from utils.GeneratePDF import fillpdf

from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
import aiogram.utils.markdown as md
from utils.logger import log

import re

userstate = gt()


@dp.message_handler(Command("Заполнение_в_телеграме"))
async def getuserdata(message: types.Message):
    log("tried to use 'in_telegram_input' option of /data command", message)
    with open("Accounts/Ubasic.csv", "rt", encoding="utf-8") as ubas:
        ishere = False
        ubas.seek(0)
        for line in ubas:
            if str(message.from_user.id) == line.rstrip():
                ishere = True
                break
    if ishere:
        log("started 'in_telegram_input' option of /data command", message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True).add("Мужской",
                                                                                                             "Женский")
        await message.answer("Начал записывать данные. Чтобы прервать действие нажмите /end")
        await message.answer("Выберите свой пол", reply_markup=markup)
        await userstate.getgender.set()
    else:
        log("failed to use 'in_telegram_input' option of /data command (no permission)", message)
        await message.answer("Нет доступа. Купите через /pay", reply_markup=types.ReplyKeyboardRemove())


# ---------------------------------------------------------------------------------------------------------------------

@dp.message_handler(state=userstate.getgender)
async def gender(message: types.Message, state: FSMContext):
    if message.text.lower() in ['мужской', 'женский']:
        # БЕЗ ЭТОГО НЕ ПРОПАДАЕТ КНОПКА ПОСЛЕ ИСПОЛЬЗОВАНИЯ
        await bot.send_message(message.chat.id, "Загрузка...", reply_markup=types.ReplyKeyboardRemove())

        await state.update_data(sex={'мужской': 'Herr', 'женский': 'Frau'}[message.text.lower()])
        await gt.next()
        await message.answer("Теперь введите имя (без фамилии)")
    else:
        await message.answer("Неверный формат пола, выберите из списка")
        await userstate.getgender.set()


@dp.message_handler(state=userstate.getfname)
async def fname(message: types.Message, state: FSMContext):
    if re.compile(r'^[a-zA-Z]+$').match(message.text):
        await state.update_data(fname=message.text)
        await gt.next()
        await message.answer(f"Введите фамилию")
    else:
        await message.answer("Неверный формат имени, попробуйте снова")
        await userstate.getfname.set()


@dp.message_handler(state=userstate.getlname)
async def lname(message: types.Message, state: FSMContext):
    if re.compile(r'^[a-zA-Z]+$').match(message.text):
        await state.update_data(lname=message.text)
        await gt.next()
        await message.answer(f"Введите имя при рождении")
    else:
        await message.answer("Неверный формат фамилии, попробуйте снова")
        await userstate.getlname.set()


@dp.message_handler(state=userstate.getbname)
async def bname(message: types.Message, state: FSMContext):
    if re.compile(r'^[a-zA-Z]+$').match(message.text):
        await state.update_data(bname=message.text)
        await gt.next()
        await message.answer(f"Введите место рождения")
    else:
        await message.answer("Неверный формат имени при рождении, попробуйте снова")
        await userstate.getbname.set()


@dp.message_handler(state=userstate.getbplace)
async def bplace(message: types.Message, state: FSMContext):
    if re.compile(r'^[a-zA-Z]+$').match(message.text):
        await state.update_data(bplace=message.text)
        await gt.next()
        await message.answer(f"Введите дату рождения в формате ДД-ММ-ГГГГ")
    else:
        await message.answer("Неверный формат места рождения, попробуйте снова")
        await userstate.getbplace.set()


@dp.message_handler(state=userstate.getbdate)
async def bdate(message: types.Message, state: FSMContext):
    if re.compile(r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-((19|20)\d\d)$").match(message.text):
        await state.update_data(bdate=message.text)
        await gt.next()
        await message.answer(f"Введите страну рождения")
    else:
        await message.answer("Неверный формат даты рождения, попробуйте снова")
        await userstate.getbdate.set()


@dp.message_handler(state=userstate.getbcountry)
async def bcountry(message: types.Message, state: FSMContext):
    if re.compile(r'^[a-zA-Z]+$').match(message.text):
        await state.update_data(bcountry=message.text)
        await gt.next()
        await message.answer(f"Введите гражданство")
    else:
        await message.answer("Неверный формат страны рождения, попробуйте снова")
        await userstate.getbcountry.set()


@dp.message_handler(state=userstate.getcitizenship)
async def citizenship(message: types.Message, state: FSMContext):
    if re.compile(r'^[a-zA-Z]+$').match(message.text):
        await state.update_data(citizenship=message.text)
        await gt.next()
        await message.answer(f"Введите дату отбытия в формате ДД-ММ-ГГГГ")
    else:
        await message.answer("Неверный формат гражданства, попробуйте снова")
        await userstate.getcitizenship.set()


@dp.message_handler(state=userstate.getreisedate)
async def reisedate(message: types.Message, state: FSMContext):
    if re.compile(r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-((19|20)\d\d)$').match(message.text):
        await state.update_data(reisedate=message.text)
        await gt.next()
        await message.answer(f"Введите номер пенсионного страхования (12 чисел)")
    else:
        await message.answer("Неверный формат даты, попробуйте снова")
        await userstate.getreisedate.set()


@dp.message_handler(state=userstate.getrentvernum)
async def rentvernum(message: types.Message, state: FSMContext):
    if re.compile(r'^\d{12}$').match(message.text):
        await state.update_data(rentvernum=int(message.text))

        # -------
        async with state.proxy() as data:
            userfname, userlname = data['fname'], data['lname']
            await fillpdf(message.from_user.id, data)

        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Получить данные в PDF файле',
                                       callback_data=f'userPDFdata/HAntrag_{message.from_user.id}.pdf'))

        await message.answer(
            md.text(md.text("Документ на ваше имя составлен:", md.bold(userfname), md.bold(userlname))),
            reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        await state.finish()
        log("succesfully ended 'in_telegram_input' option of /data command", message)
        # -------
    else:
        await message.answer("Неверный формат пенсионного номера, попробуйте снова")
        await userstate.getrentvernum.set()
