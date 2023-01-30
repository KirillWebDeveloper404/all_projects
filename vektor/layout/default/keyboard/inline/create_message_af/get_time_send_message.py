from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

time_send_msg_data = CallbackData('time_send_msg_data', 'hour')


time_send_msg_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('6:00', callback_data=time_send_msg_data.new(
                hour=6
                )),
            InlineKeyboardButton('7:00', callback_data=time_send_msg_data.new(
                hour=7
                )),
            InlineKeyboardButton('8:00', callback_data=time_send_msg_data.new(
                hour=8
                )),
        ],
        [
            InlineKeyboardButton('9:00', callback_data=time_send_msg_data.new(
                hour=9
                )),
            InlineKeyboardButton('10:00', callback_data=time_send_msg_data.new(
                hour=10
                )),
            InlineKeyboardButton('11:00', callback_data=time_send_msg_data.new(
                hour=11
                )),
        ],
        [
            InlineKeyboardButton('12:00', callback_data=time_send_msg_data.new(
                hour=12
                )),
            InlineKeyboardButton('13:00', callback_data=time_send_msg_data.new(
                hour=13
                )),
            InlineKeyboardButton('14:00', callback_data=time_send_msg_data.new(
                hour=14
                )),
        ],
        [
            InlineKeyboardButton('15:00', callback_data=time_send_msg_data.new(
                hour=15
                )),
            InlineKeyboardButton('16:00', callback_data=time_send_msg_data.new(
                hour=16
                )),
            InlineKeyboardButton('17:00', callback_data=time_send_msg_data.new(
                hour=17
                )),
        ],
        [
            InlineKeyboardButton('18:00', callback_data=time_send_msg_data.new(
                hour=18
                )),
            InlineKeyboardButton('19:00', callback_data=time_send_msg_data.new(
                hour=19
                )),
            InlineKeyboardButton('20:00', callback_data=time_send_msg_data.new(
                hour=20
                )),
        ],
        [
            InlineKeyboardButton('21:00', callback_data=time_send_msg_data.new(
                hour=21
                )),
            InlineKeyboardButton('22:00', callback_data=time_send_msg_data.new(
                hour=22
                )),
            InlineKeyboardButton('23:00', callback_data=time_send_msg_data.new(
                hour=23
                )),
        ],
        [
            InlineKeyboardButton('« Назад', callback_data=time_send_msg_data.new(
                hour='back'
            ))
        ]

    ],

)
