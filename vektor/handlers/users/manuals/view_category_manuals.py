from aiogram import types

from keyboards.inline.manuals.list_cat_manuals import list_cat_manuals_dt, generate_category_manuals_kb
from keyboards.inline.manuals.list_manuals_by_cat import generate_manuals_by_cat_id_kb, list_manuals_by_cat_dt
from loader import dp


@dp.callback_query_handler(list_cat_manuals_dt.filter(pr='category'))
async def process_get_manuals_by_category(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    category_id = int(callback_data.get('cat_id'))
    keyboard = await generate_manuals_by_cat_id_kb(category_id=category_id)
    await call.message.answer('Руководства', reply_markup=keyboard)


@dp.callback_query_handler(list_manuals_by_cat_dt.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await generate_category_manuals_kb()
    await call.message.answer('Выберете категорию руководства', reply_markup=keyboard)
