from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_rate_private_club

list_rate_private_club_data = CallbackData('list_rate_pr_cl', 'id', 'pr', 'cl_id')



async def get_list_rates_private_club(club_id):
    inline_keyboard = []
    rates = get_rate_private_club(club_id)
    if len(rates) == 0:
        return None
    else:
        for rate in rates:
            inline_keyboard.append([InlineKeyboardButton(
                text=rate.name, callback_data=list_rate_private_club_data.new(id=rate.id, pr='item', cl_id=club_id)
            )])
        inline_keyboard.append([InlineKeyboardButton(
            text='Назад', callback_data=list_rate_private_club_data.new(id='None', pr='back', cl_id=club_id)
        )])
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)