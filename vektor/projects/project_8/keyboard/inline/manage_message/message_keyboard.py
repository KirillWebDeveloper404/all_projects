from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_main_keyboard_messages():
    inline_keyboard = []
    inline_keyboard.append([InlineKeyboardButton('Добавить')])
    inline_keyboard.append([InlineKeyboardButton('Изменить')])
    inline_keyboard.append([InlineKeyboardButton('« Назад')])