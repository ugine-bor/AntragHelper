from aiogram import types
from aiogram.dispatcher.filters import Command

from utils.logger import log
from utils.access import isuser

from load import dp, __, i18n

from states.getstate import GetStartLanguage as gst
from aiogram.dispatcher import FSMContext

userstate = gst()


@dp.message_handler(state=userstate.getstrtlang)
async def changestrtlang(message: types.Message, state: FSMContext):
    langs = {"English": 'en', "Deutsch": 'de', "Русский": 'ru', "فارسی": 'fa'}
    if message.text in langs:
        log("user changes language", message)
        with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/language.txt', 'wt') as data:
            data.write(langs[message.text])
        await i18n.set_user_locale(langs[message.text])
        await message.answer(__("Язык изменен на") + " " + message.text, reply_markup=types.ReplyKeyboardRemove())

        markup = types.InlineKeyboardMarkup()

        await message.answer(__('''Нажав на /basic Вы может приобрести "Базовый пакет" заполения Вашего антрага в удобной форме на сайте.
Уже через 1 минуту как результат Вы получите заполненный антраг в виде PDF файла, который будет выслан Вам на Вашу электронную почту.

Нажав на /plus Вы можете приобрести "Премиум пакет" заполнения вашего антрага. 
После оплаты вам будет предоставлен список документов, необходимых для заполения антрага, которые вы должны будете загрузить нам в этом чате в виде PDF файлов или как фото. 
Также мы составим для вас список тех документов, копии которых вы должны приложить при подачи антрага.
В течении трёх дней заполненные антраги в виде PDF файлов будут высланы на электронную почту. 
Вспомогательные пояснения вы также будете получать в процессе работы с нами.

Нажмите /info для просмотра информации о вашем аккунте.

Нажмите /help чтобы получить больше информации.'''), reply_markup=markup)
        if isuser(message.from_user.id, "NaU"):
            await message.answer(
                __("У вас есть бесплатная возможность протестировать работу бота.\nНажмите /free чтобы начать"))
        await state.finish()
    else:
        await message.answer(__("Выберите вариант из списка."))
        userstate.getstrtlang.set()


@dp.message_handler(Command("start"))
async def strt(message: types.Message):
    markup = types.ReplyKeyboardMarkup(selective=True, one_time_keyboard=True).add(types.KeyboardButton("English"))
    markup.add(types.KeyboardButton("Deutsch"))
    markup.add(types.KeyboardButton("Русский"))
    markup.add(types.KeyboardButton("فارسی"))
    await message.answer(__("Выберите язык."), reply_markup=markup)
    await userstate.getstrtlang.set()
    print("кто-то стартовал бота:", message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    log("used /start command", message)
