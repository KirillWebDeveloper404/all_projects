from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.personal_area.money.processing import payment_processing
from loader import dp
from utils.db_api.users_model import get_user_by_chat_id


@dp.callback_query_handler(text="withdraw_money")
async def withdraw_money_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.edit_text(text="Введите номер карты в формате 1111 1111 1111 1111")
    await state.set_state("input_card")


@dp.message_handler(state="input_card")
async def input_card(message: types.Message, state: FSMContext):
    card = message.text.replace(" ", "")
    if card.isdigit():

        await state.update_data(
            {
                "card": int(card)
            }

        )
        await state.set_state("input_amount")
        await message.answer("Какую сумму вы хотите вывести?")
    else:
        await message.answer("Введите правильный номер карты")


@dp.message_handler(state="input_amount")
async def input_amount(message: types.Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Неправильный формат")
        return

    user = await get_user_by_chat_id(message.from_user.id)
    amount = int(message.text)

    if user.balance >= amount:
        data = await state.get_data()
        data["amount"] = amount

        await message.answer("Платеж поставлен на обработку.")
        await payment_processing(message, data)
    else:
        await message.answer("Недостаточно средств")








