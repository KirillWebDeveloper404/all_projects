from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_categories, get_products_by_category

mu_category_data = CallbackData('mu_ctg_dt', 'us_id', 'ct_id')


async def get_product_store_mu(user_id):
    client_store = InlineKeyboardMarkup()
    for category in get_all_categories():
        if get_products_by_category(category):
            client_store.row(
                InlineKeyboardButton(category.category,
                                     callback_data=mu_category_data.new(ct_id=category.id, us_id=user_id)))
    return client_store
