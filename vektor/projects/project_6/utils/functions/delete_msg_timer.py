from aiogram import types

from loader import bot


async def delete_msg_for_timer(msg_id, chat_id):
    await bot.delete_message(chat_id=chat_id, message_id=msg_id)
