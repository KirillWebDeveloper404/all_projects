import asyncio

from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated

from loader import bot
from modules.DataBase import get_msg_pr_cl_by_id, get_users_private_club_by_day


async def send_content_private_club(message_id):
    msg = get_msg_pr_cl_by_id(message_id)
    users = get_users_private_club_by_day(msg.day)



    for user in users:
        try:
            await bot.send_message(chat_id=user.user.tg_id, text=msg.text)
            await asyncio.sleep(0.06)
        except (BotBlocked, ChatNotFound, UserDeactivated):
            pass
