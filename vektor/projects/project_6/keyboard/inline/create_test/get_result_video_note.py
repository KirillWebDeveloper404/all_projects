from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_test.all_data import create_result_back_button, create_result_delete_button

get_result_video_note_dt = CallbackData('get_result_video_note_dt', 'prefix')


async def get_video_note_result(data):
    inline_keyboard = []
    if data['video_note']:
        inline_keyboard.append(
            [InlineKeyboardButton('Поменять', callback_data=get_result_video_note_dt.new(prefix='change'))]
        )
        inline_keyboard.append(
            [InlineKeyboardButton('Удалить', callback_data=create_result_delete_button.new(prefix='video_note'))]
        )
    inline_keyboard.append(
        [InlineKeyboardButton('« Назад', callback_data=create_result_back_button.new(prefix='back'))]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
