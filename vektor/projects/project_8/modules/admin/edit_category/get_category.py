from aiogram import types

from keyboard.inline.edit_category import get_edit_category
from keyboard.inline.get_category import get_category, category_data
from loader import dp
from modules.BotKeyboards import shop_category_data, admin_shop_category
from modules.DataBase import get_category_by_id


@dp.callback_query_handler(shop_category_data.filter(prefix='edit'))
async def edit_category_shop(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await get_category()
    await call.message.edit_text('Выберете категорию', reply_markup=keyboard)


@dp.callback_query_handler(category_data.filter(prefix='category'))
async def process_get_category(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    category_id = callback_data.get('cat_id')
    category = get_category_by_id(category_id)
    keyboard = await get_edit_category(category_id)
    await call.message.edit_text(f'Категория: {category.category}', reply_markup=keyboard)


@dp.callback_query_handler(category_data.filter(prefix='back'))
async def process_get_category(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Категории', reply_markup=admin_shop_category)
