from load import dp, bot, __
from states.getstate import GetDatacsv as gtc
from utils.logger import log


@dp.callback_query_handler()
async def callback(call):
    try:
        with open(call.data, "rb") as fsend:
            log('got document name in callback', call.message)
            await bot.send_document(call.message.chat.id, fsend)
    except Exception as e:
        await bot.send_message(chat_id=call.message.chat.id, text=f"ошибка {e}")


@dp.callback_query_handler(state=gtc.getcsv)
async def callback(call):
    with open(call.data, "rb") as fsend:
        await bot.send_document(call.message.chat.id, fsend)
