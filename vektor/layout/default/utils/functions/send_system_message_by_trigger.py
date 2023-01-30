from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot
from modules.DataBase import exists_system_message_by_trigger


async def send_system_message_by_trigger(trigger, chat_id):
    message = exists_system_message_by_trigger(trigger)
    if message:
        if message.link:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Подробнее', url=message.link)]])
        else:
            keyboard = None

        if message.photo:
            await bot.send_photo(chat_id, message.photo, message.text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id, message.text, reply_markup=keyboard)
        return True
    else:
        return None