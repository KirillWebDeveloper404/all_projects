from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

accept_delete_funnels_data = CallbackData('accept_delete_funnels', 'id', 'prefix')


async def generate_accept_delete_funnels(id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Да, удалить',
                                     callback_data=accept_delete_funnels_data.new(id=id, prefix='accept'))
            ],
            [
                InlineKeyboardButton('Нет, оставить',
                                     callback_data=accept_delete_funnels_data.new(id=id, prefix='no'))
            ],
        ]
    )
