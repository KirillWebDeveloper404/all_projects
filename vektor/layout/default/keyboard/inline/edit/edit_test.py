from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .all_data import delete_something
from keyboard.inline.edit.all_data import back_for_edit
from modules.DataBase import get_all_questions

edit_test_af_data = CallbackData('edit_test_af_data', 'prefix')
edit_test_af_data_id = CallbackData('edit_test_af_data_id', 'id')


async def generate_get_test_keyboard(data):
    inline_keyboard = []
    if data['test']:
        inline_keyboard.append([InlineKeyboardButton('Поменять тест', callback_data=edit_test_af_data.new(
            prefix='change'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить тест', callback_data=delete_something.new(prefix='test'))])
    else:
        tests = get_all_questions()
        if len(tests) == 0:
            return None
        for test in tests:
            inline_keyboard.append([InlineKeyboardButton(test.text, callback_data=edit_test_af_data_id.new(
                id=test.id
            ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=back_for_edit.new(p='1'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
