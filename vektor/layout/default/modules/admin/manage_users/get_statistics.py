import datetime
import os
from typing import List

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from openpyxl import Workbook

from keyboard.inline.users.get_segment_statistics import segment_data, get_segment_keyboard
from keyboard.inline.users.main import users_main_data, users_main

from modules.Credentials import UTC_TIME_ZONE
from loader import dp, statistic
from modules.DataBase import check_bought_products, get_all_users
from utils.functions.get_users_segment import get_users


async def get_statistics_users(users: List):
    # Create Excel (.xlsx) file -----------------------------------------------
    wb = Workbook()

    # data = await get_orders()
    ws = wb.create_sheet(0)
    ws.title = 'Пользователи'
    ws.append((
        'id',
        'телеграм id',
        'Имя',
        'Телефон',
        'Зарегистрирован',
        'Тестирование',
        'Пришел с воронки',
        'Всего покупок',
        'На сумму',
        'Куплены',
    ))
    for user in users:
        id = user.id
        chat_id = user.tg_id
        name = user.name
        funnel = user.start_funnel
        phone = user.phone_number
        stage = f'{user.stage} стадия'
        if not stage:
            stage = 'Не прошел'

        register = f'{user.ts.year}-{user.ts.month}-{user.ts.day}-{user.ts.hour}-{user.ts.minute}'

        all_buys = check_bought_products(user.id)

        buys = len(all_buys)
        price = 0
        bought = ''
        if all_buys:
            for buy in all_buys:
                price += buy.price
                bought += f'{buy.product.name}, '
        else:
            buys = 0

        ws.append((id, chat_id, name, phone, register, stage, funnel, buys, price, bought))
    workbook_name = "{path}/document/users_statistics_{datetime}".format(path=statistic, datetime=datetime.datetime.now(UTC_TIME_ZONE))
    wb.save(workbook_name + ".xlsx")
    return workbook_name + ".xlsx"


@dp.callback_query_handler(users_main_data.filter(prefix='statistics'))
async def process_get_segment(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    keyboard = await get_segment_keyboard()
    await call.message.edit_text('Выберете сегмент статистики', reply_markup=keyboard)


@dp.callback_query_handler(segment_data.filter(prefix='back'))
async def process_back_keyboard(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Управление пользователями', reply_markup=users_main)


@dp.callback_query_handler(segment_data.filter())
async def process_back_keyboard(call: types.CallbackQuery, callback_data: dict):
    segment = callback_data.get('prefix')
    await call.answer(cache_time=1)
    users = await get_users(segment)
    doc = await get_statistics_users(users)
    print(doc)
    doc_f = open(doc, 'rb')
    doc_f = InputFile(doc_f)
    os.remove(doc)
    await call.message.delete()
    await call.message.answer_document(document=doc_f)
    await call.message.answer('Управление пользователями', reply_markup=users_main)
