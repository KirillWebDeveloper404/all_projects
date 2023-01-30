from aiogram import types

from keyboards.inline.admin.create_rate import process_get_create_rate
from keyboards.inline.admin.item_rate import get_item_rate_kb
from states.create_rate import CreateRate
from utils.db_api.rates_model import get_rate_by_id


async def process_get_info_rate(data):
    text = f'Название: {data.get("name")}\n' \
           f'Цена: {data.get("price")} РУБ\n' \
           f'Путь к боту: {data.get("path")}\n' \
           f'Описание:\n{data.get("desc")}'
    return text


async def send_info_by_create_rate(data, message: types.Message, is_delete=False):
    text = await process_get_info_rate(data)
    if is_delete:
        await message.delete()

    await CreateRate.process.set()
    keyboard = await process_get_create_rate(data)
    await message.answer(text, reply_markup=keyboard)


async def send_item_rate(rate_id, message: types.Message, is_delete=False):
    rate = await get_rate_by_id(rate_id=rate_id)
    text = f'Название: {rate.name}\n' \
           f'Цена: {rate.price} РУБ\n' \
           f'Описание:\n{rate.desc}'

    keyboard = await get_item_rate_kb(rate.id)

    if is_delete:
        await message.delete()

    await message.answer(text, reply_markup=keyboard)
