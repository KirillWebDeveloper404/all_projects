from aiogram import types

from handlers.admin.payment.message import send_message_about_successful_processing
from keyboards.inline.personal_area.profile import paid
from loader import dp

# Обработка платежа на вывод
from utils.db_api.users_model import update_balance


@dp.callback_query_handler(paid.filter())
async def payment_processing(call: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get("chat_id"))
    amount = int(callback_data.get("amount"))
    await update_balance(int(chat_id), amount, deduct=True)
    await send_message_about_successful_processing(call, chat_id, amount)
    await call.message.edit_text("Выплата обработана успешно. Партнеру отправлено сообщение.")
