from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

create_af_data = CallbackData('create_af_data', 'prefix')


async def create_auto_funnel_keyboard(data=None) -> InlineKeyboardMarkup:
    """
    Клавиатура:
    + Имя
    + старт
    [+ Продукт] || [+ условие купил] [ + Условие не купил]
    [Сохранить]
    """
    if data:
        if data['fast_start'] or data['start_on_day_month'] or data['start_on_week'] or data['start_on_week'] == 0:
            start = True
        else:
            start = None
        name = data['name']
        product = data['product']
        buy = data['if_buy']
        not_buy = data['if_not_buy']
    else:
        name = None
        product = None
        buy = None
        not_buy = None
        start = None
    inline_keyboard = []

    if name:
        inline_keyboard.append([InlineKeyboardButton(text='✏️ Имя', callback_data=create_af_data.new(prefix='name'))])
        if start:
            inline_keyboard.append(
                [InlineKeyboardButton(text='✏️ старт', callback_data=create_af_data.new(prefix='start'))])
        else:
            inline_keyboard.append(
                [InlineKeyboardButton(text='➕ старт', callback_data=create_af_data.new(prefix='start'))])

    else:
        inline_keyboard.append([InlineKeyboardButton(text='➕ Имя', callback_data=create_af_data.new(prefix='name'))])
        if start:
            inline_keyboard.append(
                [InlineKeyboardButton(text='✏️ старт', callback_data=create_af_data.new(prefix='start'))])
        else:
            inline_keyboard.append(
                [InlineKeyboardButton(text='➕ старт', callback_data=create_af_data.new(prefix='start'))])

    if name and start:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='💾 Сохранить', callback_data=create_af_data.new(prefix='save')),
                InlineKeyboardButton(text='Отменить', callback_data=create_af_data.new(prefix='cancel')),
            ]
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='Отменить', callback_data=create_af_data.new(prefix='cancel')),
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
