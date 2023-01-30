from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import delete_something

msg_send_time_data = CallbackData('msg_send_time_data', 'prefix')


async def generate_get_msg_send_time_keyboard(data):
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton('Поменять время отправки', callback_data=msg_send_time_data.new(
        prefix='change_send_time'
    ))])
    inline_keyboard.append([InlineKeyboardButton('Удалить время отправки', callback_data=delete_something.new(
        thing='day%%hour'
    ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_send_time_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
