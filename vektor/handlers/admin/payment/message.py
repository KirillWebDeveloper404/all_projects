from aiogram import types


async def send_message_about_successful_processing(call: types.CallbackQuery, chat_id: int or str, amount: int):

    await call.bot.send_message(chat_id, text=f"Ваша заявка на выплату обработана успешно на {amount} RUB ")