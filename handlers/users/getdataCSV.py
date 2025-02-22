from load import dp, __

from aiogram.dispatcher.filters import Command
from aiogram import types
from states.getstate import GetDatacsv as gtc
from states.getstate import Getmail as getmailstate
from aiogram.dispatcher import FSMContext

from utils.access import isuser, reduce
from utils.logger import log

import os.path
from time import sleep
import json
from csv import DictReader as reader
import requests

from data.config import staff

userstate = gtc()
mailstate = getmailstate()


async def urlpost(msg, mode):
    data = msg.to_python()
    url = "https://145.249.247.109:8443/BotAntragTest/hs/bots/Post"  # "https://httpbin.org/anything"
    with open(f"UserFiles/U_{msg.from_user.id}/DataNotToShow/language.txt", "rt", encoding="utf-8") as fin:
        lang = fin.read()

    with open(f"UserFiles/U_{msg.from_user.id}/DataNotToShow/U_mail_{msg.from_user.id}.json", "rt",
              encoding="utf-8") as fin:
        mail = json.load(fin)
    #try:
        if mode == 3:
            with open(f'UserFiles/U_{msg.from_user.id}/DataNotToShow/files_id.csv', 'rt', encoding='utf-8') as fin:
                rd = reader(fin)
                fileids = [row['fileid'] for row in rd]

            req = requests.post(url, json={"mode": 3, "lang": lang, "email": mail['email'],
                                           "partner": mail.get('partner', None),
                                           "message": {**data, **{'document': {'file_id': fileids}}}},
                                verify=False)  # "message": data | {'document': {'file_id': fileids}}
        else:
            req = requests.post(url, json={"mode": mode, "lang": lang, "email": mail['email'],
                                           "partner": mail.get('partner', None), "message": data}, verify=False)
        log(f"POST request done. result: {req.status_code}", msg)
        if req.status_code != 200:
            await msg.answer(
                __("Что-то пошло не так при отправке файла.\nОшибка {}.\nЗагрузите файл ещё или отмените действие нажав /end.".format(
                    req.status_code)))
            await userstate.getcsv.set()
            raise ConnectionError
    #except Exception as e:
    #    await msg.answer(__(f"Ошибка при отправке запроса: {str(e)}"))
    return


@dp.message_handler(Command("data"))
async def getuserdatacsv(message: types.Message):
    log("tried to use 'Sample_csv' option of /data command", message)
    if message.from_user.id in staff or isuser(message.from_user.id, "basic"):
        await message.answer(__("Загрузите .xlsx ли .xls файл.\nЧтобы отменить действие нажмите /end."),
                             reply_markup=types.ReplyKeyboardRemove())
        await userstate.getcsv.set()
        log("started 'Sample_csv' option of /data command", message)
    else:
        log("failed to use 'Sample_csv' option of /data command (no permission)", message)
        await message.answer(__("Нет доступа.\nКупите через /pay."), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['document'], state=userstate.getfreecsv)
async def csvfreefile(message: types.Message, state: FSMContext):
    if message.document.file_name.endswith(".xlsx") or message.document.file_name.endswith(".xls"):
        if len([name for name in os.listdir(f"UserFiles/U_{message.from_user.id}/DataVisible") if
                os.path.isfile(name)]) < 95:
            await message.document.download(
                destination_file=f"UserFiles/U_{message.from_user.id}/DataVisible/{message.document.file_name}")

            ishere = False
            for i in range(1, 10):
                if os.path.exists(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.document.file_name}"):
                    ishere = True
                    break
                else:
                    sleep(2)
            if ishere:
                log("succesfully uploaded .xlsx file using 'Sample_xlsx' option of /free command", message)
                try:
                    # Extract data from .csv to dict
                    # with open(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.document.file_name}",
                    #           encoding="utf-8") as fin:
                    #     datacsv = {}
                    #     data = fin.read()
                    #     for line in data.splitlines():
                    #         l = line.split(';')
                    #         datacsv[l[0]] = l[1]

                    await message.answer(__("Файл {} получен.\nПодождите немного, пока собирается документ.").format(
                        message.document.file_name))

                    await urlpost(message, mode=1)  # POST request; mode=1 - free

                    await message.answer(__("Запрос отправлен.\nЗаполненный пример скоро придет на почту"))

                    log("succesfully ended 'Sample_csv' option of /free command", message)
                    await state.finish()

                    return
                except UnicodeDecodeError:
                    log("UnicodeDecodeError ('Sample_csv' option of /free command)", message)
                    await message.answer(
                        __("Повреждённый файл. Провверьте правильность заполненных данных. \nПопробуйте загрузить файл снова"))
                    await userstate.getfreecsv.set()
                    log("asked to upload .csv once again because of UnicodeDecodeError ('Sample_csv' option of /free command)",
                        message)
                except Exception as e:
                    log(f"{e} ('Sample_csv' option of /free command)", message)
                    await message.answer(__("Неизвестная ошибка. Попробуйте загрузить файл снова"))
                    print(e)
                    await userstate.getfreecsv.set()
                    log(f"asked to upload .csv once again because of {e} error ('Sample_csv' option of /free command)",
                        message)
            else:
                await message.answer(__("Что-то пошло не так. Загрузите файл ещё раз."))
                await userstate.getfreecsv.set()
                log("asked to upload .csv once again because of upload timeout error ('Sample_csv' option of /freefi command)",
                    message)

        else:
            await message.answer(__("Слишком много файлов"))
            log("failed to upload .csv . Too much files in user folder ('Sample_csv' option of /free command)", message)
    else:
        await message.answer(__("Не тот тип файла, опробуйте снова.\nНужен .csv"))
        await userstate.getfreecsv.set()
        log("asked to upload .csv once again because of file type error ('Sample_csv' option of /free command)",
            message)


@dp.message_handler(content_types=['document'], state=userstate.getcsv)
async def csvfile(message: types.Message, state: FSMContext):
    if message.document.file_name.endswith(".xlsx") or message.document.file_name.endswith(".xls"):
        if len([name for name in os.listdir(f"UserFiles/U_{message.from_user.id}/DataVisible") if
                os.path.isfile(name)]) < 20:
            await message.document.download(
                destination_file=f"UserFiles/U_{message.from_user.id}/DataVisible/{message.document.file_name}")

            ishere = False
            for i in range(1, 10):
                if os.path.exists(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.document.file_name}"):
                    ishere = True
                    break
                else:
                    sleep(2)
            if ishere:
                log("succesfully uploaded .xlsx file using 'Sample_csv' option of /data command", message)
                try:

                    await message.answer(__("Файл {} получен.\nПодождите немного, пока собирается документ.").format(
                        message.document.file_name))

                    await urlpost(message, mode=2)  # post request; mode=2 -basic

                    log("succesfully ended 'Sample_csv' option of /data command", message)
                    # -1 access to command
                    if not (message.from_user.id in staff):
                        reduce(message.from_user.id, usertype="basic")
                    log("-1 access of basic command ('Sample_csv' option of /data command)", message)
                    await message.answer("Готово.\nСкоро результат придёт на почту.")
                    await state.finish()

                    return

                except UnicodeDecodeError:
                    log("UnicodeDecodeError ('Sample_csv' option of /data command)", message)
                    await message.answer(
                        __("Повреждённый файл. Провверьте правильность заполненных данных. \nПопробуйте загрузить файл снова"))
                    await userstate.getcsv.set()
                    log("asked to upload .csv once again because of UnicodeDecodeError ('Sample_csv' option of /data command)",
                        message)
                except ConnectionError:
                    await message.answer(
                        __("При отправке запроса произошла ошибка.\nПопробуйте снова нажав /data."))
                except Exception as e:
                    log(f"{e} ('Sample_csv' option of /data command)", message)
                    await message.answer(__("Неизвестная ошибка. Попробуйте загрузить файл снова"))
                    print(e)
                    await userstate.getcsv.set()
                    log(f"asked to upload .csv once again because of {e} error ('Sample_csv' option of /data command)",
                        message)
            else:
                await message.answer(__("Что-то пошло не так.\nЗагрузите файл ещё или отмените действие нажав /end ."))
                await userstate.getcsv.set()
                log("asked to upload .xlsx once again because of upload timeout error ('Sample_csv' option of /data command)",
                    message)

        else:
            await message.answer(__("Слишком много файлов"))
            log("failed to upload .xlsx . Too much files in user folder ('Sample_csv' option of /data command)", message)
    else:
        await message.answer(__("Не тот тип файла, опробуйте снова.\nНужен .xlsx"))
        await userstate.getcsv.set()
        log("asked to upload .xlsx once again because of file type error ('Sample_csv' option of /data command)",
            message)
