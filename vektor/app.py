
from aiogram import executor, types

from loader import dp, scheduler
import middlewares, filters, handlers
from scheduler.start import setup_scheduler
from utils.db_api import setup_db
from utils.notify_admins import on_startup_notify
from utils.rates.add_rates_default import add_rates_test
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Создаем таблицы в БД
    await setup_db()

    # Добавляем пробный период
    await add_rates_test()

    # # Подключаемся к базам данных
    # await connect_databases_bots()

    # Запускаем задачи
    await setup_scheduler(dispatcher)

    #
    # # Уведомляет про запуск
    # await on_startup_notify(dispatcher)

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
