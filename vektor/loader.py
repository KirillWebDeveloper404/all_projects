from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token='1938072901:AAFqXxn9Ew-CPm55o8Wt-eA9MfaaRYXBIMM', parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
bots_manager = 0
scheduler = 0
