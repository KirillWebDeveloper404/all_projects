from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

job_af_data = CallbackData('job_af_data', 'prefix')


async def get_job_buy_do(buy=False, data=False):
    inline_keyboard = []

    if buy:
        inline_keyboard.append([InlineKeyboardButton('Остановить', callback_data=job_af_data.new(prefix='stop'))])
        inline_keyboard.append([InlineKeyboardButton('Редирект', callback_data=job_af_data.new(prefix='redirect'))])
        if data:
            if not data['created']:
                inline_keyboard.append(
                    [InlineKeyboardButton('Пропустить шаг', callback_data=job_af_data.new(prefix='skip_buy'))])
    else:
        inline_keyboard.append(
            [InlineKeyboardButton('Редирект', callback_data=job_af_data.new(prefix='redirect_not_buy'))])
        if data:
            if not data['created']:
                inline_keyboard.append(
                    [InlineKeyboardButton('Пропустить шаг', callback_data=job_af_data.new(prefix='skip_not_buy'))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
