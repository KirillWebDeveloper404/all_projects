from aiogram import types

from handlers.admin.manuals.get_manual_info import get_manuals_info_by_view_admin
from keyboards.inline.admin.category_manuals import category_manuals_data
from keyboards.inline.admin.category_manuals_manage import category_manuals_manage_data, \
    generate_category_manuals_manage_kb
from keyboards.inline.admin.view_manual import generate_manual_view_admin_kb, view_manual_admin_dt
from loader import dp
from utils.db_api.categories_manuals_model import get_category_manual_by_id


@dp.callback_query_handler(category_manuals_manage_data.filter(pr='manual'))
async def process_view(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    manual_id = int(callback_data.get('ml_id'))
    category_id = int(callback_data.get('cat_id'))
    text = await get_manuals_info_by_view_admin(manual_id)
    keyboard = await generate_manual_view_admin_kb(category_id=category_id, manual_id=manual_id)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(view_manual_admin_dt.filter(pr='back'))
async def process_back(call: types.CallbackQuery, callback_data: dict):
    category_id = int(callback_data.get('cat_id'))
    await call.answer(cache_time=1)
    category = await get_category_manual_by_id(category_id=category_id)
    text = f'Категория: {category.name}\n'
    keyboard = await generate_category_manuals_manage_kb(category_id)
    await call.message.edit_text(text, reply_markup=keyboard)
