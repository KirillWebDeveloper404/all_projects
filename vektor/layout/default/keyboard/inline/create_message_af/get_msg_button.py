from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import delete_something

msg_button_data = CallbackData('msg_button_data', 'prefix')


async def generate_get_msg_button_change_keyboard():
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton('Поменять кнопку', callback_data=msg_button_data.new(
        prefix='change_button_link'
    ))])
    inline_keyboard.append([InlineKeyboardButton('Удалить кнопку', callback_data=delete_something.new(
        thing='link%%text_link'
    ))])
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_button_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def generate_get_msg_button_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton('« Назад', callback_data=msg_button_data.new(prefix='back'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
