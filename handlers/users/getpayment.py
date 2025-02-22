from aiogram.dispatcher import FSMContext

from load import dp, bot, __
from utils.access import newuser, adder, isuser

from aiogram import types
from utils.logger import log

from re import compile
from os.path import exists

from states.getstate import Getmail as gm
from states.getstate import GetDatacsv as gtc

import json

userstate = gm()
getfreestate = gtc()


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == "basic":
        log("Successful payment (basic)", message)
        if isuser(message.from_user.id, usertype="basic", nul=True):
            adder(message.from_user.id, usertype="basic", howmuch=2)

            await message.reply(__('''Платеж успешно принят! Спасибо за оплату!

Перейдите на сайт https://alexsoft.kz:8443/hab/ для заполнения антрага.

Добавлено 2 доступа к командам Basic.

Подробнее о командах в /help.'''))

            log("+2 access to commands (basic)", message)
        elif not isuser(message.from_user.id, usertype="basic", nul=True):
            newuser(message.from_user.id, usertype="basic", howmuch=2)

            await message.reply(__('''Платеж успешно принят! Спасибо за оплату!

Перейдите на сайт https://alexsoft.kz:8443/hab/ для заполнения антрага.

Добавлено 2 доступа к командам Basic.

Разблокирована функция /data.

Подробнее о командах в /help.'''))

            log("Added new user to (basic)", message)

        if exists(f"UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json"):
            with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json',
                      'r') as fin:
                email_now = json.load(fin)['email']

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True).add(
                __("Да"),
                __("Нет"))
            await message.answer(__("У вас уже есть записанный email {}. Хотите изменить его?").format(email_now),
                                 reply_markup=markup)
            await userstate.mailagain.set()
            log(f"Asked if user want to change email '{email_now}' after payment", message)
        else:
            await bot.send_message(message.chat.id, __("Введите email чтобы продолжить"))
            await userstate.getmail.set()
    elif message.successful_payment.invoice_payload == "premium":
        log("Successful payment (premium)", message)
        if isuser(message.from_user.id, usertype="premium", nul=True):
            adder(message.from_user.id, usertype="premium", howmuch=1)

            await message.reply(__('''Платеж успешно принят! Спасибо за оплату!

Перейдите на сайт https://alexsoft.kz:8443/hab/ для загрузки документов.

Добавлен 1 доступ к командам premium.

Подробнее о командах в /help.'''))

            log("+1 access to commands (premium)", message)
        elif not isuser(message.from_user.id, usertype="premium", nul=True):
            newuser(message.from_user.id, usertype="premium", howmuch=1)

            await message.reply(__('''Платеж успешно принят! Спасибо за оплату!

Перейдите на сайт https://alexsoft.kz:8443/hab/ для загрузки документов.

Добавлен 1 доступ к командам Premium.

Разблокированы команды /upload, /show, /delete.

Подробнее о командах в /help.'''))

            log("Added new user to (premium)", message)

        if exists(f"UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json"):
            with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json',
                      'r') as fin:
                email_now = json.load(fin)['email']

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True).add(
                __("Да"),
                __("Нет"))
            await message.answer(__("У вас уже есть записанный email {}. Хотите изменить его?").format(email_now),
                                 reply_markup=markup)
            await userstate.mailagain.set()
            log(f"Asked if user want to change email '{email_now}' after payment", message)
        else:
            await message.answer(__("Введите email чтобы продолжить."))
            await userstate.getmail.set()
            log("Asked for email after payment", message)


@dp.message_handler(state=userstate.mailagain)
async def grabemailagain(message: types.Message, state: FSMContext):
    if message.text == __("Да"):
        await message.answer(__("Введите почту заново."), reply_markup=types.ReplyKeyboardRemove())
        await userstate.getmail.set()
        log(f"user wants to change mail (mail)", message)
    elif message.text == __("Нет"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True).add(__("Нет"))
        await message.answer(__("Почта осталась прежней."), reply_markup=markup)
        await bot.send_message(message.chat.id,
                               __("Введите код партнёра если он есть.\n Если его нет, или вы не знаете что это такое то нажмите 'Нет'"))
        await userstate.getpartnercode.set()
        log(f"user doesnt wants to change mail (mail)", message)
    else:
        await message.answer(__("Выберите Да или Нет"))
        log(f"user responded wrong. Ask to choose from given variants (mail)", message)


@dp.message_handler(state=userstate.getmail)
async def grabemail(message: types.Message, state: FSMContext):
    log(f"try to add {message.text} as (mail)", message)
    if compile(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])").match(
        message.text):
        await state.update_data(email=message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True).add(__("Да"),
                                                                                                             __("Нет"))
        await message.answer(__('Подтвердите, что это ваша почта: {}').format(message.text), reply_markup=markup)
        await userstate.checkmail.set()
        log(f"{message.text} can be used as (mail)", message)
    else:
        log(f"cant add {message.text} as (mail)", message)
        await message.answer(__("Неверный формат почты, попробуйте снова."))
        await userstate.getmail.set()


@dp.message_handler(state=userstate.checkmail)
async def checkpost(message: types.Message, state: FSMContext):
    if message.text == __("Да"):
        log(f"user confirmed '{message.text}' (mail)", message)
        mail = await state.get_data('email')
        with open(f"UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json", "wt",
                  encoding="utf-8") as fout:
            json.dump({"id": f"{message.from_user.id}", "email": f"{mail['email']}"}, fout)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True).add(__("Нет"))

        await message.answer(__("Почта записана."), reply_markup=markup)

        await bot.send_message(message.chat.id,
                               __("Введите код партнёра если он есть.\n Если его нет, или вы не знаете что это такое то нажмите 'Нет'"))

        await userstate.getpartnercode.set()
    elif message.text == __("Нет"):
        await message.answer(__("Введите почту заново."), reply_markup=types.ReplyKeyboardRemove())
        await userstate.getmail.set()
        log(f"user rejected '{message.text}'. Ask to write mail again (mail)", message)
    else:
        await message.answer(__("Выберите 'Да' или 'Нет'."))
        log(f"user responded wrong to checker ({message.text}). Ask to choose from given variants (mail)", message)


@dp.message_handler(state=userstate.getpartnercode)
async def grabpartner(message: types.Message, state: FSMContext):
    if message.text == __("Нет"):
        if isuser(message.from_user.id, "premium"):
            await message.answer(
                __("Можете начать загружать необходимые для обработки документы.\nДля этого используйте команду /upload."),
                reply_markup=types.ReplyKeyboardRemove())

            await state.finish()
        elif isuser(message.from_user.id, "basic"):
            await message.answer(
                __("Можете начать работу с заполнением документов.\nДля этого Используйте команду /data."),
                reply_markup=types.ReplyKeyboardRemove())

            await state.finish()
        else:

            if isuser(message.from_user.id, "NaU"):
                await message.answer(__("Загрузите .csv файл.\nЧтобы отменить действие нажмите /end."),
                                     reply_markup=types.ReplyKeyboardRemove())
                log("started /free command after email verification", message)
                await getfreestate.getfreecsv.set()
                return
            else:
                log("failed to use /free command (no permission)", message)
                await message.answer(__("Нет доступа.\nКоманда уже использована или у вас уже есть купленная услуга."),
                                     reply_markup=types.ReplyKeyboardRemove())

                await state.finish()
    elif compile(r"[-A-Za-z0-9]+").match(message.text):
        with open(f"UserFiles/U_{message.from_user.id}/DataNotToShow/U_mail_{message.from_user.id}.json", "r+t",
                  encoding="utf-8") as fin:
            data = json.load(fin)
            data.update({'partner': message.text})
            fin.seek(0)
            json.dump(data, fin)

        if isuser(message.from_user.id, "premium"):
            await message.answer(
                __("Можете начать загружать необходимые для обработки документы.\nДля этого используйте команду /upload."),
                reply_markup=types.ReplyKeyboardRemove())

            await state.finish()
        elif isuser(message.from_user.id, "basic"):
            await message.answer(
                __("Можете начать работу с заполнением документов.\nДля этого Используйте команду /data."),
                reply_markup=types.ReplyKeyboardRemove())

            await state.finish()
        else:

            if isuser(message.from_user.id, "NaU"):
                await message.answer(__("Загрузите .csv файл.\nЧтобы отменить действие нажмите /end."),
                                     reply_markup=types.ReplyKeyboardRemove())
                log("started /free command after email verification", message)
                await getfreestate.getfreecsv.set()
                return
            else:
                log("failed to use /free command (no permission)", message)
                await message.answer(__("Нет доступа.\nКоманда уже использована или у вас уже есть купленная услуга."),
                                     reply_markup=types.ReplyKeyboardRemove())

                await state.finish()
    else:
        await message.answer(__("Неверный формат кода.\nПопробуйте ввести email снова."))
        await userstate.getpartnercode.set()
    await state.finish()
