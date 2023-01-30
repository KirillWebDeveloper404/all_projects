from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_products_by_category

af_product_data = CallbackData('af_product_data', 'id')


async def get_products(category):
    client_store = InlineKeyboardMarkup()
    for product in get_products_by_category(category):
        client_store.row(
            InlineKeyboardButton(product.name, callback_data=af_product_data.new(id=product.id)))
    return client_store
