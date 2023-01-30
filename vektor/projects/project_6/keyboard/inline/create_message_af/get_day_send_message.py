from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

day_send_msg_data = CallbackData('day_send_msg_data', 'day')


async def get_day_send_msg_kb(data: dict):
    if data['type'] == 'system':
        text_1 = 'За 1 день'
        text_2 = 'За 2 дня'
        text_3 = 'За 3 дня'
        text_4 = 'За 4 дня'
        text_5 = 'За 5 дней'
        text_6 = 'За 6 дней'
        text_7 = 'За 7 дней'
        text_8 = 'За 8 дней'
        text_9 = 'За 9 дней'
        text_10 = 'За 10 дней'
        text_11 = 'За 11 дней'
        text_12 = 'За 12 дней'
        text_13 = 'За 13 дней'
        text_14 = 'За 14 дней'
        text_15 = 'За 15 дней'
    else:
        text_1 = 'день 1'
        text_2 = 'день 2'
        text_3 = 'день 3'
        text_4 = 'день 4'
        text_5 = 'день 5'
        text_6 = 'день 6'
        text_7 = 'день 7'
        text_8 = 'день 8'
        text_9 = 'день 9'
        text_10 = 'день 10'
        text_11 = 'день 11'
        text_12 = 'день 12'
        text_13 = 'день 13'
        text_14 = 'день 14'
        text_15 = 'день 15'


    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text_1, callback_data=day_send_msg_data.new(
                    day=1
                )),
                InlineKeyboardButton(text_2, callback_data=day_send_msg_data.new(
                    day=2
                )),
                InlineKeyboardButton(text_3, callback_data=day_send_msg_data.new(
                    day=3
                )),
            ],
            [
                InlineKeyboardButton(text_4, callback_data=day_send_msg_data.new(
                    day=4
                )),
                InlineKeyboardButton(text_5, callback_data=day_send_msg_data.new(
                    day=5
                )),
                InlineKeyboardButton(text_6, callback_data=day_send_msg_data.new(
                    day=6
                )),
            ],
            [
                InlineKeyboardButton(text_7, callback_data=day_send_msg_data.new(
                    day=7
                )),
                InlineKeyboardButton(text_8, callback_data=day_send_msg_data.new(
                    day=8
                )),
                InlineKeyboardButton(text_9, callback_data=day_send_msg_data.new(
                    day=9
                )),
            ],
            [
                InlineKeyboardButton(text_10, callback_data=day_send_msg_data.new(
                    day=10
                )),
                InlineKeyboardButton(text_11, callback_data=day_send_msg_data.new(
                    day=11
                )),
                InlineKeyboardButton(text_12, callback_data=day_send_msg_data.new(
                    day=12
                )),
            ],
            [
                InlineKeyboardButton(text_13, callback_data=day_send_msg_data.new(
                    day=13
                )),
                InlineKeyboardButton(text_14, callback_data=day_send_msg_data.new(
                    day=14
                )),
                InlineKeyboardButton(text_15, callback_data=day_send_msg_data.new(
                    day=15
                )),
            ],
            [
                InlineKeyboardButton('« Назад', callback_data=day_send_msg_data.new(
                    day='back'
                ))
            ]
        ]
    )