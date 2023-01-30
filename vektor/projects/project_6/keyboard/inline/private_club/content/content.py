from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_categories_by_club_id

content_pr_cl_data = CallbackData('content_pr_club', 'cl_id', 'pr')

async def get_content_pr_cl_kb(club_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Список уроков', callback_data=content_pr_cl_data.new(cl_id=club_id, pr='list'))
            ],
            [
                InlineKeyboardButton('Добавить новый урок', callback_data=content_pr_cl_data.new(cl_id=club_id, pr='new'))
            ],
            [
                InlineKeyboardButton('Назад', callback_data=content_pr_cl_data.new(cl_id=club_id, pr='back'))
            ],
        ]
    )