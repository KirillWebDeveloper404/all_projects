from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from modules.DataBase import get_all_rates_by_course_id

course_list_rates_data = CallbackData('course_list_rates', 'cr_id', 'rt_id', 'pr')


async def get_rate_list_course_kb(course_id):
    rates = get_all_rates_by_course_id(course_id)
    inline_keyboard = []
    if len(rates) == 0:
        return None
    else:
        for rate in rates:
            inline_keyboard.append([InlineKeyboardButton(rate.name, callback_data=course_list_rates_data.new(
                cr_id=course_id, rt_id=rate.id, pr='item'
            ))])
        inline_keyboard.append([InlineKeyboardButton('Назад', callback_data=course_list_rates_data.new(
            cr_id=course_id, rt_id='0', pr='back'
        ))])
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
