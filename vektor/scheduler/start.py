from aiogram import Dispatcher

from loader import scheduler
from scheduler.period import check_free_trial_period


async def setup_scheduler(dp: Dispatcher):
    scheduler.add_job(check_free_trial_period, "interval", days=1, args=(dp,))