from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_private_club

view_pr_cl = CallbackData('fffview_pr-club', 'club_id')


async def process_get_all_pr_club():
    clubs = get_all_private_club()
    inline_keyboard = InlineKeyboardMarkup()
    for club in clubs:
        inline_keyboard.row(InlineKeyboardButton(text=club.name, callback_data=view_pr_cl.new(club_id=club.id)))
    return inline_keyboard
