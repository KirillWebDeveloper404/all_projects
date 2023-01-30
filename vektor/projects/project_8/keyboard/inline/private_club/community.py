from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_private_club_by_id

community_pr_club = CallbackData('community_pr_club', 'club_id', 'pr')


async def get_community_pr_club(club_id):
    club = get_private_club_by_id(club_id=club_id)
    inline_keyboard = []
    if club.channel:
        inline_keyboard.append(
            [InlineKeyboardButton(text='✔️ Канал', callback_data=community_pr_club.new(club_id=club.id, pr='channel'))])
    else:
        inline_keyboard.append(
            [InlineKeyboardButton(text='Канал', callback_data=community_pr_club.new(club_id=club.id, pr='channel'))])

    if club.private_chat:
        inline_keyboard.append(
            [InlineKeyboardButton(text='✔️ Чат', callback_data=community_pr_club.new(club_id=club.id, pr='chat'))])
    else:
        inline_keyboard.append(
            [InlineKeyboardButton(text='Чат', callback_data=community_pr_club.new(club_id=club.id, pr='chat'))])

    inline_keyboard.append(
        [InlineKeyboardButton(text='Назад', callback_data=community_pr_club.new(club_id=club.id, pr='back'))])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)