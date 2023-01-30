from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_private_club

list_private_club_data = CallbackData('lest_private_club', 'id', 'pr')


async def get_list_private_clubs():
    inline_keyboard = []
    clubs = get_all_private_club()
    if len(clubs) == 0:
        return None
    else:
        for club in clubs:
            inline_keyboard.append([InlineKeyboardButton(
                text=club.name, callback_data=list_private_club_data.new(id=club.id, pr='item')
            )])
        inline_keyboard.append([InlineKeyboardButton(
            text='Назад', callback_data=list_private_club_data.new(id='None', pr='back')
        )])

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)