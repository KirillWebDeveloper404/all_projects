from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import delete_something
from modules.DataBase import get_all_questions

msg_test_af_data = CallbackData('msg_test_af_data', 'prefix')
msg_test_af_data_id = CallbackData('msg_test_af_data_id', 'id')


async def generate_get_test_keyboard(data):
    inline_keyboard = []
    if data['test']:
        inline_keyboard.append([InlineKeyboardButton('Поменять тест', callback_data=msg_test_af_data.new(
            prefix='change_test'
        ))])
        inline_keyboard.append([InlineKeyboardButton('Удалить тест', callback_data=delete_something.new(thing='test'))])
    else:
        tests = get_all_questions()
        if len(tests) == 0:
            return None
        for test in tests:
            inline_keyboard.append([InlineKeyboardButton(test.text, callback_data=msg_test_af_data_id.new(
                id=test.id
            ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_test_af_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
