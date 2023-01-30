from aiogram import types

from keyboards.inline.admin.rates_main import rates_main, rates_main_data
from keyboards.inline.admin.start import admin_data, admin_start
from loader import dp


@dp.callback_query_handler(admin_data.filter(pr='rates'))
async def process_start(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Тарифы', reply_markup=rates_main)


@dp.callback_query_handler(rates_main_data.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Админ-панель', reply_markup=admin_start)
