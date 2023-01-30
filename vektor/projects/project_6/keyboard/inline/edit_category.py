from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

edit_category_data = CallbackData('edit_category_data', 'cat_id', 'prefix')


async def get_edit_category(category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Название', callback_data=edit_category_data.new(
                    cat_id=category_id,
                    prefix='category'
                ))
            ],
            [
                InlineKeyboardButton('« Назад', callback_data=edit_category_data.new(
                    cat_id=category_id,
                    prefix='back'
                ))
            ]
        ],
    )
