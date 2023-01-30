from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bots_manager


@dp.message_handler(Command('delete_all'))
async def process_delete(message: types.Message):
    await bots_manager.__delete_all_projects__()
    await message.answer('Все проекты успешно удалены')
