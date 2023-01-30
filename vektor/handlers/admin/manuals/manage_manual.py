from aiogram import types

from keyboards.inline.admin.category_manuals_manage import generate_category_manuals_manage_kb
from keyboards.inline.admin.view_manual import view_manual_admin_dt
from loader import dp
from utils.db_api.categories_manuals_model import get_category_manual_by_id
from utils.db_api.manuals_model import delete_manual_by_id


@dp.callback_query_handler(view_manual_admin_dt.filter(pr='delete'))
async def process_back(call: types.CallbackQuery, callback_data: dict):
    manual_id = int(callback_data.get('ml_id'))
    category_id = int(callback_data.get('cat_id'))
    await call.answer(cache_time=1)
    await delete_manual_by_id(manual_id)
    category = await get_category_manual_by_id(category_id=category_id)
    text = f'Категория: {category.name}\n'
    keyboard = await generate_category_manuals_manage_kb(category_id)
    await call.message.edit_text(text, reply_markup=keyboard)
