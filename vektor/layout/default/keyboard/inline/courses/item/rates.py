from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

rates_courses_data = CallbackData('rate_cr', 'cr', 'pr')


async def get_rates_course_main_kb(course_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Список тарифов', callback_data=rates_courses_data.new(
                    cr=course_id, pr='list'
                ))
            ],
            [
                InlineKeyboardButton(text='Создать новый', callback_data=rates_courses_data.new(
                    cr=course_id, pr='new'
                ))
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=rates_courses_data.new(
                    cr=course_id, pr='back'
                ))
            ],
        ]
    )
