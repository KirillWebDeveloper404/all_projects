from aiogram import types

from keyboards.inline.admin.category_manuals import category_manuals_data, generate_category_manuals_kb
from keyboards.inline.admin.category_manuals_manage import generate_category_manuals_manage_kb, \
    category_manuals_manage_data
from loader import dp
from utils.db_api.categories_manuals_model import get_category_manual_by_id


@dp.callback_query_handler(category_manuals_data.filter(pr='category'))
async def process_get_category(call: types.CallbackQuery, callback_data: dict):
    category_id = int(callback_data.get('cat_id'))
    await call.answer(cache_time=1)
    category = await get_category_manual_by_id(category_id=category_id)
    text = f'Категория: {category.name}\n'
    keyboard = await generate_category_manuals_manage_kb(category_id)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(category_manuals_manage_data.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await generate_category_manuals_kb()
    await call.message.edit_text('Категории', reply_markup=keyboard)
