import asyncio
from typing import List

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from modules.DataBase import get_lessons_for_free_intensive


@dp.message_handler(Command('get_all_lessons'), user_id=[1691530315, 690812581])
async def get_all_lessons(message: types.Message):
    lessons = get_lessons_for_free_intensive()
    for lesson in lessons:
        text = f'{lesson.day} {lesson.time}\n\n' \
               f'Сообщение:\n' \
               f'{lesson.text_lesson}'
        await message.answer(text)
        await asyncio.sleep(1)
