from datetime import datetime, timedelta

import pytz
from aiogram import Dispatcher

from data.config import TIME_ZONE
from loader import bots_manager
from utils.db_api.projects_model import get_project_is_not_payment
from utils.db_api.users_model import select_users_free_active, update_status_free_active


async def check_free_trial_period(dp: Dispatcher):
    users = await select_users_free_active(free_active=True)
    timezone_default = pytz.timezone(TIME_ZONE)
    date_now_format = datetime.now(timezone_default).strftime("%Y-%M-%D")
    for user in users:
        free_activate = timedelta(user.free_days)
        end_date = (user.ts + free_activate).strftime("%Y-%M-%D")
        if end_date == date_now_format:
            projects = await get_project_is_not_payment(user.chat_id, True)
            await update_status_free_active(user.chat_id, False)
            for project in projects:
                await bots_manager.__off_status__(project.id)

            await dp.bot.send_message(chat_id=user.chat_id, text="Пробный период закончился. Все проекты, которые не были оплачены, приостановлены")




