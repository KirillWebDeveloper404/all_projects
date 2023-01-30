from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_categories

category_data = CallbackData('category_data', 'cat_id', 'prefix')


async def get_category():
    client_store = InlineKeyboardMarkup()
    for category in get_all_categories():
        client_store.row(InlineKeyboardButton(category.category, callback_data=category_data.new(cat_id=category.id,
                                                                                                 prefix='category')))
    client_store.row(InlineKeyboardButton('« Назад', callback_data=category_data.new(cat_id='None', prefix='back')))
    return client_store
