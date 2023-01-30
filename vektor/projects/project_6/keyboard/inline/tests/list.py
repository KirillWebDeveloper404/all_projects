from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_questions

list_tests_data = CallbackData('list_tests_data', 'id')


async def generate_list_tests_keyboard():
    inline_keyboard = []
    questions = get_all_questions()
    if questions:
        for question in questions:
            inline_keyboard.append(
                [InlineKeyboardButton(text=question.text, callback_data=list_tests_data.new(id=question.id))])

    inline_keyboard.append([InlineKeyboardButton(text='« Назад', callback_data=list_tests_data.new(id='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)