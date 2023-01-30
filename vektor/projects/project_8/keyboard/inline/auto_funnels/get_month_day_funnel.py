from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

month_day_funnel_data = CallbackData('month_day_funnel', 'day')

month_day_funnel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('1', callback_data=month_day_funnel_data.new(day=1)),
            InlineKeyboardButton('2', callback_data=month_day_funnel_data.new(day=2)),
            InlineKeyboardButton('3', callback_data=month_day_funnel_data.new(day=3)),
            InlineKeyboardButton('4', callback_data=month_day_funnel_data.new(day=4)),
            InlineKeyboardButton('5', callback_data=month_day_funnel_data.new(day=5)),
            InlineKeyboardButton('6', callback_data=month_day_funnel_data.new(day=6)),
            InlineKeyboardButton('7', callback_data=month_day_funnel_data.new(day=7)),
        ],
        [
            InlineKeyboardButton('8', callback_data=month_day_funnel_data.new(day=8)),
            InlineKeyboardButton('9', callback_data=month_day_funnel_data.new(day=9)),
            InlineKeyboardButton('10', callback_data=month_day_funnel_data.new(day=10)),
            InlineKeyboardButton('11', callback_data=month_day_funnel_data.new(day=11)),
            InlineKeyboardButton('12', callback_data=month_day_funnel_data.new(day=12)),
            InlineKeyboardButton('13', callback_data=month_day_funnel_data.new(day=13)),
            InlineKeyboardButton('14', callback_data=month_day_funnel_data.new(day=14)),
        ],
        [
            InlineKeyboardButton('15', callback_data=month_day_funnel_data.new(day=15)),
            InlineKeyboardButton('16', callback_data=month_day_funnel_data.new(day=16)),
            InlineKeyboardButton('17', callback_data=month_day_funnel_data.new(day=17)),
            InlineKeyboardButton('18', callback_data=month_day_funnel_data.new(day=18)),
            InlineKeyboardButton('19', callback_data=month_day_funnel_data.new(day=19)),
            InlineKeyboardButton('20', callback_data=month_day_funnel_data.new(day=20)),
            InlineKeyboardButton('21', callback_data=month_day_funnel_data.new(day=21)),
        ],
        [
            InlineKeyboardButton('22', callback_data=month_day_funnel_data.new(day=22)),
            InlineKeyboardButton('23', callback_data=month_day_funnel_data.new(day=23)),
            InlineKeyboardButton('24', callback_data=month_day_funnel_data.new(day=23)),
            InlineKeyboardButton('25', callback_data=month_day_funnel_data.new(day=25)),
            InlineKeyboardButton('26', callback_data=month_day_funnel_data.new(day=26)),
            InlineKeyboardButton('27', callback_data=month_day_funnel_data.new(day=27)),
            InlineKeyboardButton('28', callback_data=month_day_funnel_data.new(day=28)),
        ],
    ]
)