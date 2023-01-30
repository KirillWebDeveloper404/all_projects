from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import delete_something

msg_interval_data = CallbackData('msg_interval_data', 'prefix')


async def generate_get_msg_interval_keyboard(data):
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton('Поменять задержку', callback_data=msg_interval_data.new(
        prefix='change_interval'
    ))])
    inline_keyboard.append([InlineKeyboardButton('Удалить время отправки', callback_data=delete_something.new(
        thing='interval_timer'
    ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_interval_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
