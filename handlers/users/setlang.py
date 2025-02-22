from load import dp, i18n, __

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from utils.logger import log

from states.getstate import GetLanguage

userstate = GetLanguage()


@dp.message_handler(Command('lang'))
async def handlang(message: types.Message):
    markup = types.ReplyKeyboardMarkup(selective=True, one_time_keyboard=True).add(types.KeyboardButton("English"))
    markup.add(types.KeyboardButton("Deutsch"))
    markup.add(types.KeyboardButton("Русский"))
    markup.add(types.KeyboardButton("فارسی"))
    await message.answer(__("Выберите язык."), reply_markup=markup)
    await userstate.getlang.set()


@dp.message_handler(state=userstate.getlang)
async def changelang(message: types.Message, state: FSMContext):
    langs = {"English": 'en', "Deutsch": 'de', "Русский": 'ru', "فارسی": 'fa'}
    if message.text in langs:

        log("user changes language", message)
        with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/language.txt', 'wt') as data:
            data.write(langs[message.text])
        await i18n.set_user_locale(langs[message.text])
        await message.answer(__("Язык изменен на") + " " + message.text, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(__("Выберите вариант из списка."))
        userstate.getlang.set()
