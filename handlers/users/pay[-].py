from load import dp, bot, __
from data.config import stripe_token

from aiogram.dispatcher.filters import Command
from aiogram import types
from utils.logger import log


@dp.message_handler(Command("pay"))
async def pay(message: types.Message):
    log(f"used /pay command", message)
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(__('Оплатить'), pay=True))
    markup.add(types.InlineKeyboardButton(__('Посмотреть на сайте'), url='https://alexsoft.kz:8443/hab/'))
    await bot.send_invoice(message.chat.id, __("Базовая услуга"),
                           __("Купить базовый пакет для автоматического заполнения антрагов на основе шаблона. Получение доступа к функции /data. Подробнее о функциях в /help."),
                           "basic",
                           stripe_token, "EUR",
                           prices=[types.LabeledPrice(__('Стоимость'), 5 * 100 + 99)],
                           photo_url="https://global-uploads.webflow.com/62d84b3d3ba446b2ec041a19/62d84b3d3ba446ca2e04463e_basic%20pay.jpeg",
                           reply_markup=markup)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Someone tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")
