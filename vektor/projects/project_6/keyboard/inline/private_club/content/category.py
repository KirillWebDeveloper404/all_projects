from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_categories_by_club_id

category_pr_cl_data = CallbackData('cat_pr_cl', 'cat_id')
category_all_pr_cl_data = CallbackData('cat_all_pr_cl', 'cat_id', 'cl_id')


async def get_category_club_kb(club_id):
    categories = get_all_categories_by_club_id(club_id)
    inline_keyboard = []
    for category in categories:
        inline_keyboard.append([InlineKeyboardButton(category.name, callback_data=category_pr_cl_data.new(
            cat_id=category.id
        ))])
    inline_keyboard.append([InlineKeyboardButton('Добавить новую', callback_data=category_pr_cl_data.new(
        cat_id='new'
    ))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



async def get_main_category_club_kb(club_id):
    categories = get_all_categories_by_club_id(club_id)
    inline_keyboard = []
    if len(categories) == 0:
        return None
    for category in categories:
        inline_keyboard.append([InlineKeyboardButton(category.name, callback_data=category_all_pr_cl_data.new(
            cat_id=category.id, cl_id=club_id
        ))])

    inline_keyboard.append([InlineKeyboardButton('Создать новую', callback_data=category_all_pr_cl_data.new(
        cat_id='new', cl_id=club_id
    ))])
    inline_keyboard.append([InlineKeyboardButton('Назад', callback_data=category_all_pr_cl_data.new(
        cat_id='back', cl_id=club_id
    ))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)