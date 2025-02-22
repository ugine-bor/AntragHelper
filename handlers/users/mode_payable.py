from aiogram.dispatcher import FSMContext

from load import dp, bot, __

from aiogram.dispatcher.filters import Command
from aiogram import types
from aiogram.types.web_app_info import WebAppInfo

from utils.access import isuser
from utils.logger import log


@dp.message_handler(Command("free"))
async def free(message: types.Message, state: FSMContext):
    if isuser(message.from_user.id, "NaU", nul=True):

        log("used /free command", message)

        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(__('Перейти на сайт'), url='http://alexsoft.kz:5000/'))
        markup.add(types.InlineKeyboardButton("Внутри телеграма(тест)",
                                       web_app=WebAppInfo(url="http://alexsoft.kz:5000/")))
        await message.answer(__("Нажмите на кнопку ниже чтобы перейти на страницу заполнения."), reply_markup=markup)

        # await mailstate.getmail.set()
    else:
        await message.answer(__("У вас уже есть купленная опция."))


@dp.message_handler(Command("basic"))
async def pay(message: types.Message):
    log(f"used /basic command", message)
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(__('Перейти на сайт'), url='https://alexsoft.kz:8443/hab/product/hauptantrag?pa_sposob_zapolneniya=samostoyatelno'))
    markup.add(types.InlineKeyboardButton("Внутри телеграма(тест)",
                                          web_app=WebAppInfo(url="https://alexsoft.kz:8443/hab/product/hauptantrag?pa_sposob_zapolneniya=samostoyatelno")))
    await message.answer(__("Нажмите на кнопку ниже чтобы перейти на страницу заполнения."), reply_markup=markup)


@dp.message_handler(Command("plus"))
async def payplus(message: types.Message):
    log(f"used /basic command", message)
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(__('Перейти на сайт'), url='https://alexsoft.kz:8443/hab/product/hauptantrag?pa_sposob_zapolneniya=specialistom'))
    markup.add(types.InlineKeyboardButton("Внутри телеграма(тест)",
                                          web_app=WebAppInfo(url="https://alexsoft.kz:8443/hab/product/hauptantrag?pa_sposob_zapolneniya=specialistom")))
    await message.answer(__("Нажмите на кнопку ниже чтобы перейти на страницу заполнения."), reply_markup=markup)
