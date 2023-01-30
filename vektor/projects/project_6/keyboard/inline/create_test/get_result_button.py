from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_test.all_data import create_result_back_button, create_result_delete_button

get_result_button_dt = CallbackData('get_result_button_dt', 'prefix')


async def get_button_result(data):
    inline_keyboard = []
    if data['link'] and data['text_link']:
        inline_keyboard.append(
            [InlineKeyboardButton('Поменять', callback_data=get_result_button_dt.new(prefix='change'))]
        )
        inline_keyboard.append(
            [InlineKeyboardButton('Удалить',
                                  callback_data=create_result_delete_button.new(prefix='link%%text_link'))]
        )
    inline_keyboard.append(
        [InlineKeyboardButton('« Назад', callback_data=create_result_back_button.new(prefix='back'))]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
