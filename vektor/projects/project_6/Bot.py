from logging_start import logging
from modules.Config import DELAY
import asyncio

import aioschedule
from aiogram.utils import executor

from modules import dp
from loader import scheduler
# async def update_timetable():
#     logging.debug("Started every-minute polling")
#     remove_unactual_events()
#     await send_notifications_of_classes()

from modules.DataBase import get_lessons_for_free_intensive, get_all_message_friday_vebinar, update_days_users_af, \
    update_days_users_pr_club
from modules.free_intensive.function import sending_lesson, starting_free_intensive, update_users_days, \
    sending_message_vebinar
from utils import set_default_command


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


async def scheduler_func():
    # Начнет пользователю бесплатный интенсив
    aioschedule.every().monday.at("01:00").do(starting_free_intensive)

    # Создает расписание отправки уроков
    lessons = get_lessons_for_free_intensive()
    for lesson in lessons:
        aioschedule.every().day.at(lesson.time).do(
            sending_lesson,
            lesson.day,
            lesson.text_lesson,
            lesson.photo_text,
            lesson.gif_text,
            lesson.id,
            lesson.audio_text,
        )

    friday_message = get_all_message_friday_vebinar()
    for message in friday_message:
        aioschedule.every().friday.at(message.time).do(
            sending_message_vebinar,
            message.message_text,
            message.photo_text,
            message.gif_text,
            message.audio_text,
            message.time_vebinar,
            message.id
        )

    # Увеличивает день пользователя на 1
    aioschedule.every().day.at("23:59").do(update_users_days)
    aioschedule.every().day.at("23:59").do(update_days_users_af)
    aioschedule.every().day.at("23:59").do(update_days_users_pr_club)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler_func())
    await set_default_command(dp)

if __name__ == "__main__":
    import filters

    logging.info("BotStarted")
    loop = asyncio.get_event_loop()

    scheduler.start()
    # loop.call_later(DELAY, repeat, update_timetable, loop)
    executor.start_polling(dp, skip_updates=True, loop=loop, on_startup=on_startup)
