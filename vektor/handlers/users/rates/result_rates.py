from aiogram import types

from loader import dp
from utils.db_api.rates_model import get_all_rates


@dp.message_handler(text="💵 Тарифы")
async def rates(message: types.Message):
    rates_db = await get_all_rates()
    text_with_rates = "\n\n".join([
        f"<b>Тариф</b> №{number}\n"
        f"Название: {rate.name}\n"
        f"Цена: {rate.price} RUB\n"
        f"Описание: {rate.desc}"
        for number, rate in enumerate(rates_db, 1)
        if not rate.id == 1]
    )
    await message.answer(f"💵 Тарифы\n\n{text_with_rates}")
