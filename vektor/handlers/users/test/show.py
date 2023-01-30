from aiogram import types

from keyboards.inline import start_data
from loader import dp


@dp.callback_query_handler(start_data.filter(pr="show"))
async def show_handler(call: types.CallbackQuery):
    await call.message.edit_text("Тут будет видео")
