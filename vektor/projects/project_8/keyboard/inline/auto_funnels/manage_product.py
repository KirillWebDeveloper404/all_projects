from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

af_manage_product_data = CallbackData('af_manage_product_data', 'prefix')


async def af_manage_product(data):
    inline_keyboard = []

    if data['product']:
        inline_keyboard.append([InlineKeyboardButton(text='Поменять продукт',
                                                     callback_data=af_manage_product_data.new(prefix='set'))])

        inline_keyboard.append([InlineKeyboardButton(text='Удалить продукт',
                                                     callback_data=af_manage_product_data.new(prefix='delete'))])
    else:
        inline_keyboard.append([InlineKeyboardButton(text='Добавить продукт',
                                                     callback_data=af_manage_product_data.new(prefix='set'))])
    if not data['created']:
        inline_keyboard.append([InlineKeyboardButton(text='Пропустить шаг',
                                                     callback_data=af_manage_product_data.new(prefix='skip'))])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
