from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# создание основный макрообъектов для обращения к боту
from modules.Credentials import BOT_TOKEN, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB, TIME_ZONE

bot = Bot(token=BOT_TOKEN)
ms = MemoryStorage()
dp = Dispatcher(bot, storage=ms)
url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB}'
statistic = Path(__file__).parent

jobstores = {
    'default': SQLAlchemyJobStore(url=url, tableschema='public')
}

scheduler = AsyncIOScheduler({'apscheduler.timezone': TIME_ZONE}, jobstores=jobstores)

