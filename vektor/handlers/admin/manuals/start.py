from aiogram import types

from keyboards.inline.admin.category_manuals import generate_category_manuals_kb, category_manuals_data
from keyboards.inline.admin.start import admin_data, admin_start
from loader import dp


@dp.callback_query_handler(admin_data.filter(pr='manuals'))
async def process_start(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await generate_category_manuals_kb()
    await call.message.edit_text('Категории', reply_markup=keyboard)


@dp.callback_query_handler(category_manuals_data.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Админ-панель', reply_markup=admin_start)
