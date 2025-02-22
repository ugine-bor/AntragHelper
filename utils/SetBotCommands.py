from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [types.BotCommand('help', 'Detailed description of each command'),
         types.BotCommand('pay', 'Basic service'),
         types.BotCommand('payplus', 'Premium service'),
         types.BotCommand('info', 'Information about your account'),
         types.BotCommand('lang', 'Set bot language')])
