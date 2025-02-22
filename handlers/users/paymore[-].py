from load import dp, bot, __
from data.config import stripe_token
from utils.logger import log

from aiogram.dispatcher.filters import Command
from aiogram import types


@dp.message_handler(Command("payplus"))
async def paymuch(message: types.Message):
    log(f"used /payplus command", message)
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(__('Оплатить'), pay=True))
    markup.add(types.InlineKeyboardButton(__('Посмотреть на сайте'), url='https://alexsoft.kz:8443/hab/'))
    await bot.send_invoice(message.chat.id, __("Премиум услуга"),
                           __("Купить премиум пакет для автоматического заполнения антрагов на основе загруженных документов. Получение доступа к функциям /data /upload /show /request. Подробнее о функциях в /help."),
                           "premium", stripe_token, "EUR",
                           prices=[types.LabeledPrice('Стоимость', 14 * 100 + 99)],
                           photo_url="https://www.lobsters.at/wp-content/uploads/2017/01/premium.jpg",
                           reply_markup=markup)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Someone tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")
