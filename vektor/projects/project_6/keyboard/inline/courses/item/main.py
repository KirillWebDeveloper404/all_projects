from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

course_item_data = CallbackData('ссcourse_item', 'cr', 'pr')

async def course_item_kb(course_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Тарифы', callback_data=course_item_data.new(
                    cr=course_id, pr='rate'
                )),
                InlineKeyboardButton(text='Настройки', callback_data=course_item_data.new(
                    cr=course_id, pr='settings'
                )),
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data=course_item_data.new(
                    cr=course_id, pr='back'
                )),
                InlineKeyboardButton(text='Удалить', callback_data=course_item_data.new(
                    cr=course_id, pr='del'
                )),
            ],
        ]
    )