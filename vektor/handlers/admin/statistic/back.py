from aiogram import types

from keyboards.inline.admin.back_statistic import statistics_data
from keyboards.inline.admin.start import admin_start
from loader import dp


@dp.callback_query_handler(statistics_data.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Админ-панель', reply_markup=admin_start)