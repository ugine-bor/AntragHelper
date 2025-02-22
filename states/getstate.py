from aiogram.dispatcher.filters.state import StatesGroup, State


class GetStartLanguage(StatesGroup):
    getstrtlang = State()


class GetLanguage(StatesGroup):
    getlang = State()


class Getmail(StatesGroup):
    mailagain = State()
    getmail = State()
    checkmail = State()
    getpartnercode = State()


class GetFileState(StatesGroup):
    uploadfile = State()
    showfile = State()
    deletefile = State()


class GetDatacsv(StatesGroup):
    getfreecsv = State()
    getcsv = State()


class GetDataState(StatesGroup):
    getgender = State()
    getfname = State()
    getlname = State()
    getbname = State()
    getbplace = State()
    getbdate = State()
    getbcountry = State()
    getcitizenship = State()
    getreisedate = State()
    getrentvernum = State()
