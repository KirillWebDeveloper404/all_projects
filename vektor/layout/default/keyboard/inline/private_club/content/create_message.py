from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_categories_by_club_id

create_message_pr_cl_data = CallbackData('create_message_pr_cl', 'pr')

async def create_message(data: dict):
    inline_keyboard = []
    row_1 = []
    row_2 = []
    row_3 = []

    row_1.append(InlineKeyboardButton('Категории', callback_data=create_message_pr_cl_data.new(pr='category')))
    row_1.append(InlineKeyboardButton('Время', callback_data=create_message_pr_cl_data.new(pr='time')))
    row_2.append(InlineKeyboardButton('Контент', callback_data=create_message_pr_cl_data.new(pr='content')))
    if data['content'] and data['hour']:
        row_2.append(InlineKeyboardButton('Сохранить', callback_data=create_message_pr_cl_data.new(pr='save')))
    if not data['edit']:
        row_3.append(InlineKeyboardButton('Закончить (не сохранит текущее)', callback_data=create_message_pr_cl_data.new(pr='cancel')))
    inline_keyboard.append(row_1)
    inline_keyboard.append(row_2)
    inline_keyboard.append(row_3)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
