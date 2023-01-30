from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

view_rates_club = CallbackData('bbbview_rate_in_club_id', 'rate_id')


async def get_rates_buy_club(rates: List):
    keyboard = InlineKeyboardMarkup()
    for rate in rates:
        keyboard.row(InlineKeyboardButton(rate.name, callback_data=view_rates_club.new(rate_id=rate.id)))
    return keyboard
