from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_categories, get_products_by_category

af_category_data = CallbackData('af_category_data', 'id')


async def get_product_store():
    client_store = InlineKeyboardMarkup()
    for category in get_all_categories():
        if get_products_by_category(category):
            client_store.row(
                InlineKeyboardButton(category.category, callback_data=af_category_data.new(id=category.id)))
    return client_store
