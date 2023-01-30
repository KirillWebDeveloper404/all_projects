from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_test.all_data import create_result_back_button, create_result_delete_button
from modules.DataBase import get_all_question_without_question

get_result_test_dt = CallbackData('get_result_test_dt', 'prefix')
get_result_test_qs_dt = CallbackData('get_result_test_dt', 'id')


async def get_tests_result(data):
    inline_keyboard = []
    if data['test']:
        inline_keyboard.append(
            [InlineKeyboardButton('Поменять', callback_data=get_result_test_dt.new(prefix='change'))]
        )
        inline_keyboard.append(
            [InlineKeyboardButton('Удалить', callback_data=create_result_delete_button.new(prefix='test'))]
        )
    else:
        tests = get_all_question_without_question(data['question_id'])
        if len(tests) == 0:
            return None
        for test in tests:
            inline_keyboard.append([InlineKeyboardButton(test.text, callback_data=get_result_test_qs_dt.new(
                id=test.id
            ))])
    inline_keyboard.append(
        [InlineKeyboardButton('« Назад', callback_data=create_result_back_button.new(prefix='back'))]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
