from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from .all_datas import add_field_rate_private_club

create_rate_pr_club = CallbackData('create_rate_pr_club_dt', 'pr', 'cl_id')


async def get_create_rate_main_kb(data: dict):
    inline_keyboard = []
    row_1 = []  # Название || описание
    row_2 = []  # Медиа || Демо
    row_3 = []  # Период || Цена
    row_4 = []  # Сохранить и опубликовать
    row_5 = []  # Отменить создание
    if data['name']:
        row_1.append(InlineKeyboardButton(
            text='✔️ Название',
            callback_data=add_field_rate_private_club.new(pr='name', cl_id=data['club_id'], rt_id='None')
        ))
    else:
        row_1.append(InlineKeyboardButton(
            text='Название',
            callback_data=add_field_rate_private_club.new(pr='name', cl_id=data['club_id'], rt_id='None')
        ))

    if data['desc']:
        row_1.append(InlineKeyboardButton(
            text='✔️ Описание',
            callback_data=add_field_rate_private_club.new(pr='desk', cl_id=data['club_id'], rt_id='None')
        ))
    else:
        row_1.append(InlineKeyboardButton(
            text='Описание',
            callback_data=add_field_rate_private_club.new(pr='desk', cl_id=data['club_id'], rt_id='None')
        ))

    if data['media']:
        row_2.append(InlineKeyboardButton(
            text='✔️ Медиа',
            callback_data=add_field_rate_private_club.new(pr='media', cl_id=data['club_id'], rt_id='None')
        ))
    else:
        row_2.append(InlineKeyboardButton(
            text='Медиа',
            callback_data=add_field_rate_private_club.new(pr='media', cl_id=data['club_id'], rt_id='None')
        ))

    if data['demo']:
        row_2.append(InlineKeyboardButton(
            text='✔️ Демо',
            callback_data=add_field_rate_private_club.new(pr='demo', cl_id=data['club_id'], rt_id='None')
        ))
    else:
        row_2.append(InlineKeyboardButton(
            text='Демо',
            callback_data=add_field_rate_private_club.new(pr='demo', cl_id=data['club_id'], rt_id='None')
        ))

    if data['time']:
        row_3.append(InlineKeyboardButton(
            text='✔️ Период',
            callback_data=add_field_rate_private_club.new(pr='time', cl_id=data['club_id'], rt_id='None')
        ))
    else:
        row_3.append(InlineKeyboardButton(
            text='Период',
            callback_data=add_field_rate_private_club.new(pr='time', cl_id=data['club_id'], rt_id='None')
        ))

    if data['price']:
        row_3.append(InlineKeyboardButton(
            text='✔️ Цена',
            callback_data=add_field_rate_private_club.new(pr='price', cl_id=data['club_id'], rt_id='None')
        ))
    else:
        row_3.append(InlineKeyboardButton(
            text='Цена',
            callback_data=add_field_rate_private_club.new(pr='price', cl_id=data['club_id'], rt_id='None')
        ))

    if data['price'] and data['desc'] and data['time'] and data['name']:
        row_4.append(InlineKeyboardButton(text='Сохранить и опубликовать', callback_data=create_rate_pr_club.new(
            pr='save', cl_id=data['club_id']
        )))

    row_5.append(InlineKeyboardButton(text='Отменить создание', callback_data=create_rate_pr_club.new(
        pr='cancel', cl_id=data['club_id']
    )))

    inline_keyboard.append(row_1)
    inline_keyboard.append(row_2)
    inline_keyboard.append(row_3)
    inline_keyboard.append(row_4)
    inline_keyboard.append(row_5)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
