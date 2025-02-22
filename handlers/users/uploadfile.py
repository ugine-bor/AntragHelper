from os import listdir, remove
import os.path

from aiogram import types
from aiogram.dispatcher.filters import Command

from states.getstate import GetFileState as gf
from load import dp, bot, __
from utils.access import isuser
from utils.logger import log
from csv import writer, reader

userstate = gf()


def filekeyboard(uid):
    markup = types.ReplyKeyboardMarkup().add("/end")
    with open(f"UserFiles/U_{uid}/DataNotToShow/files_id.csv", 'r', newline='') as fin:
        rd = reader(fin)
        next(rd)
        [markup.add(types.KeyboardButton(row[0])) for row in rd if row]
    return markup


@dp.message_handler(state=userstate.showfile)
async def get_file(message: types.Message):
    file_id = None
    with open(f"UserFiles/U_{message.from_user.id}/DataNotToShow/files_id.csv", 'r') as fin:
        rd = reader(fin)
        next(rd)
        for row in rd:
            if row[0] == message.text:
                file_id = row[1]
    if not file_id:
        await message.answer(__("Нет такого файла.\nПопробуй снова или нажми /end."))
        return
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, f"UserFiles/U_{message.from_user.id}/DataVisible/{message.text}")
    try:
        if message.text.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '-')):
            with open(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.text}", "rb") as fsend:
                await bot.send_photo(message.chat.id, fsend)
        else:
            with open(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.text}", "rb") as fsend:
                await bot.send_document(message.chat.id, fsend)
        log(f"successfully sended {message.text} file (/show)", message)
        os.remove(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.text}")
    except IOError as e:
        await message.answer(__("Ошибка доступа к файлу.\nПопробуй снова или нажми /end."))
        log(f"failed to send file {str(e)} (/show)", message)
        return
    except Exception as e:
        log(f"failed to send file {str(e)} (/show)", message)
        await message.answer(__("Ошибка.\nПопробуй снова или нажми /end."))
        return


@dp.message_handler(Command("show"))
async def seedata(message: types.Message):
    log("used /show command", message)
    if isuser(message.from_user.id, "premium", nul=True):
        await message.answer(__('''Выберите файл, который хотите получить.
Вы можете удалить файлы с помощию команды /delete.
Вы можете загрузить файлы с помощью /upload.
Чтобы закончить действие нажмите /end.

Чтобы подать запрос на обработку ваших загруженных файлов используйте /request.'''),
                             reply_markup=filekeyboard(message.from_user.id))
        await userstate.showfile.set()
        log("successfully started /show command", message)
    else:
        log("failed to use /show command (no permission)", message)
        await message.answer(__("В доступе отказано. Купите через /payplus."))


@dp.message_handler(Command("upload"))
async def getfiles(message: types.Message):
    log("used /upload command", message)
    if isuser(message.from_user.id, "premium"):
        await message.answer(__('''Загрузите документы или фото.
Лимит на возможное количество файлов - 20 штук.
Вы можете загружать .zip архивы.
Вы можете просмотреть загруженные файлы с помощию команды /show.
Вы можете удалить файлы с помощию команды /delete.

Чтобы подать запрос на обработку ваших загруженных файлов используйте /request.'''))
    else:
        log("failed to use /upload command (no permission)", message)
        await message.answer(__("В доступе отказано. Купите через /payplus."))


@dp.message_handler(content_types=['photo', 'document'])
async def processfiles(message: types.Message):
    log("start to process users file (/upload)", message)
    if isuser(message.from_user.id, "premium"):
        try:
            try:
                filename = message.document.file_name
            except:
                if message.document:
                    filename = message.document.file_name
                else:
                    filename = message.photo[-1]
            if message.content_type == 'photo':
                await message.answer(__("Загружаю '{}'").format(filename["file_unique_id"]))
                log(f"downloading file {filename} (/upload)", message)
                with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/files_id.csv', 'a',
                          encoding='utf-8', newline='') as fout:
                    csv_writer = writer(fout)
                    csv_writer.writerow((filename["file_unique_id"], filename["file_id"]))
            elif message.content_type == 'document':
                await message.answer(__("Загружаю '{}'").format(filename))
                log(f"downloading file {filename} (/upload)", message)

                with open(f'UserFiles/U_{message.from_user.id}/DataNotToShow/files_id.csv', 'a',
                          encoding='utf-8', newline='') as fout:
                    csv_writer = writer(fout)
                    csv_writer.writerow((filename, message.document.file_id))
            else:
                await message.answer(__("Недопустимый файл '{}'").format(filename))
                log("failed to upload file. Not a file (/upload)", message)
        except AttributeError as e:
            await message.answer(__("Недопустимый файл."))
            log(f"failed to upload file. AttributeError (/upload) {e}", message)
        except Exception as e:
            await message.answer(__("Неизвестная ошибка, попробуйте снова."))
            log(f"failed to upload file. {e} error (/upload)", message)
            print(e)


@dp.message_handler(Command("delete"))
async def deletefiles(message: types.Message):
    log("used /delete command", message)
    if isuser(message.from_user.id, "premium", nul=True):
        await message.answer(__('''Выберите файл, который хотите удалить.
Вы можете просмотреть оставшиеся файлы с помощию команды /show.
Чтобы закончить действие нажмите /end.

Чтобы подать запрос на обработку ваших загруженных файлов используйте /request.'''),
                             reply_markup=filekeyboard(message.from_user.id))
        await userstate.deletefile.set()
        log("successfully started /delete command", message)
    else:
        log("failed to use /delete command (no permission)", message)
        await message.answer(__("В доступе отказано. Купите через /payplus"))


@dp.message_handler(state=userstate.deletefile)
async def todelete(message: types.Message):
    try:
        if os.path.exists(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.text}"):
            remove(f"UserFiles/U_{message.from_user.id}/DataVisible/{message.text}")
            await message.answer(__("Удаляю файл '{}'").format(message.text),
                                 reply_markup=filekeyboard(message.from_user.id))
            log(f"successfully deleted file {message.text} (/delete)", message)
        else:
            log(f"failed to delete file {message.text}. No such file (/delete)", message)
            await message.answer(__("Нет такого файла '{}'").format(message.text),
                                 reply_markup=filekeyboard(message.from_user.id))
    except Exception as e:
        log(f"failed to delete file {message.text}. {e} error (/delete)", message)
        await message.answer(__("Ошибка:") + str(e))
