from aiogram import types

from data.config import CHAT_ID
from keyboards.inline.personal_area.profile import paid_for_partner


async def payment_processing(message: types.Message, data):
    card = data.get("card")
    amount = data.get("amount")

    text = f"""
Запрос на вывод от <a href='{message.from_user.url}'>{message.from_user.full_name}</a>
Сумма: {amount}
Номер карты: {card}
"""
    await message.bot.send_message(CHAT_ID, text=text, reply_markup=paid_for_partner(message.from_user.id, amount=amount) )