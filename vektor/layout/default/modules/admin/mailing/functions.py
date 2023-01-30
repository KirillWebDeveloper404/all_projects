import asyncio
import logging
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import ChatNotFound, BotBlocked, UserDeactivated

from loader import bot, scheduler
from modules.Credentials import UTC_TIME_ZONE
from utils.functions.get_users_segment import get_users


async def send_message_users(message_text, data, image=None, document=None, animation=None, link=None, text_link=None):
    users = await get_users(data)
    keyboard = None
    if link:
        if text_link:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text_link, url=link)]])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Ссылка', url=link)]])

    if image:
        for user in users:
            try:
                await bot.send_photo(chat_id=user.tg_id, photo=image, caption=message_text, reply_markup=keyboard)
                await asyncio.sleep(0.1)
            except (ChatNotFound, BotBlocked, UserDeactivated):
                logging.warning(f"Impossible to notify {user.tg_id}")
        return
    if document:
        for user in users:
            try:
                await bot.send_document(chat_id=user.tg_id, document=document, caption=message_text,
                                        reply_markup=keyboard)
                await asyncio.sleep(0.1)
            except (ChatNotFound, BotBlocked, UserDeactivated):
                logging.warning(f"Impossible to notify {user.tg_id}")
        return
    if animation:
        for user in users:
            try:
                await bot.send_animation(chat_id=user.tg_id, animation=animation, caption=message_text,
                                         reply_markup=keyboard)
                await asyncio.sleep(0.1)
            except (ChatNotFound, BotBlocked, UserDeactivated):
                logging.warning(f"Impossible to notify {user.tg_id}")
        return

    for user in users:
        try:
            await bot.send_message(chat_id=user.tg_id, text=message_text, reply_markup=keyboard)
            await asyncio.sleep(0.1)
        except (ChatNotFound, BotBlocked, UserDeactivated):
            logging.warning(f"Impossible to notify {user.tg_id}")




async def adding_job_date(data):
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    hour = int(data['hour'])
    minute = int(data['minute'])
    message_text = data['message_text']
    data_users = data['data']
    photo = data['photo']
    document = data['document']
    animation = data['animation']
    link = data['link']
    text_link = data['text_link']

    scheduler.add_job(send_message_users, 'date',
                      run_date=datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=UTC_TIME_ZONE),
                      args=(message_text, data_users, photo, document, animation, link, text_link,),
                      name='scheduler-jobs')


async def adding_job_every(data):
    every_day = data['every_day']
    every_day_of_week = data['every_day_of_week']
    day_of_week = data['day_of_week']
    day_of_month = data['day_of_month']
    every_month = data['every_month']
    hour = int(data['hour'])
    minute = int(data['minute'])
    message_text = data['message_text']
    data_users = data['data']
    photo = data['photo']
    document = data['document']
    animation = data['animation']
    link = data['link']
    text_link = data['text_link']

    if every_day:
        # Каждый день в определенное время
        scheduler.add_job(send_message_users, 'cron', hour=hour, minute=minute,
                          args=(message_text, data_users, photo, document, animation, link, text_link,),
                          name='scheduler-jobs')

    if every_day_of_week:
        # Каждый определенный день недели в определенное время
        scheduler.add_job(send_message_users, 'cron', day_of_week=day_of_week, hour=hour, minute=minute,
                          args=(message_text, data_users, photo, document, animation, link, text_link,),
                          name='scheduler-jobs')
    if every_month:
        # Каждый месяц в определнный день
        scheduler.add_job(send_message_users, 'cron', day=day_of_month, hour=hour, minute=minute,
                          args=(message_text, data_users, photo, document, animation, link, text_link,),
                          name='scheduler-jobs')
