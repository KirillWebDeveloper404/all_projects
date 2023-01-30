from aiogram import types

from keyboards.inline.manuals.list_manuals_by_cat import list_manuals_by_cat_dt, generate_manuals_by_cat_id_kb
from keyboards.inline.manuals.view_manuals_kb import get_manual_view_kb, view_manuals_dt
from loader import dp
from .get_manual_info import get_manuals_info


@dp.callback_query_handler(list_manuals_by_cat_dt.filter(pr='manual'))
async def process_back(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    manual_id = int(callback_data.get('man_id'))
    cat_id = int(callback_data.get('cat_id'))
    text = await get_manuals_info(manual_id=manual_id)
    keyboard = await get_manual_view_kb(cat_id=cat_id)
    await call.message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(view_manuals_dt.filter(pr='back'))
async def process_back(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    cat_id = int(callback_data.get('cat_id'))
    keyboard = await generate_manuals_by_cat_id_kb(category_id=cat_id)
    await call.message.answer('Руководства', reply_markup=keyboard)
