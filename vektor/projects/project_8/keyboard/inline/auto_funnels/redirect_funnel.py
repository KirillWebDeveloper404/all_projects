from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_auto_funnels

redirect_af_data = CallbackData('redirect_af_data', 'id')


async def get_redirect():
    inline_keyboard = []
    for funnel in get_all_auto_funnels():
        inline_keyboard.append(
            [InlineKeyboardButton(f'{funnel.name}', callback_data=redirect_af_data.new(id=funnel.id))]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
