from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from modules.DataBase import get_messages_days_distinct


async def get_day_messages_keyboard():
    msgs = get_messages_days_distinct()
    inline_keyboard = []
    row = []
    for i in range(len(msgs)):
        row.append([InlineKeyboardButton(f'{msgs[i].day}', )])
        if len(msgs) == i + 1:
            inline_keyboard.append(row)
            break
        if i + 1 % 5 == 0:
            inline_keyboard.append(row)
            row = []

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)