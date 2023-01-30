from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

course_rate_item_data = CallbackData('raate_course_item', 'cr', 'rt', 'pr')


async def get_course_rate_item(course_id, rate_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Уроки', callback_data=course_rate_item_data.new(
                    cr=course_id, rt=rate_id, pr='lessons'
                )),
                InlineKeyboardButton('Изменить', callback_data=course_rate_item_data.new(
                    cr=course_id, rt=rate_id, pr='edit'
                )),
            ],
            [
                InlineKeyboardButton('Назад', callback_data=course_rate_item_data.new(
                    cr=course_id, rt=rate_id, pr='back'
                )),
                InlineKeyboardButton('Удалить', callback_data=course_rate_item_data.new(
                    cr=course_id, rt=rate_id, pr='del'
                )),
            ]
        ]
    )
