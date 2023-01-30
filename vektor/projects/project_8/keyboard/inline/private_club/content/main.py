from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

content_private_club_data = CallbackData('content_pr_cl', 'cl_id', 'pr')

async def get_content_private_club(club_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Контент', callback_data=content_private_club_data.new(cl_id=club_id, pr='content')
                )
            ],
            [
                InlineKeyboardButton(
                    'Категории', callback_data=content_private_club_data.new(cl_id=club_id, pr='category')
                )
            ],
            [
                InlineKeyboardButton(
                    'Назад', callback_data=content_private_club_data.new(cl_id=club_id, pr='back')
                )
            ],

        ]
    )