async def startup(dp):
    from utils.notify import on_startup_notify
    from utils.SetBotCommands import set_default_commands

    await on_startup_notify(dp)
    await set_default_commands(dp)
    print("Господин парсер запущен")


async def shutdown(dp):
    from utils.notify import on_shutdown_notify

    await on_shutdown_notify(dp)
    print("Господин парсер выключен")


if __name__ == '__main__':
    from handlers import dp
    from aiogram.utils import executor

    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
