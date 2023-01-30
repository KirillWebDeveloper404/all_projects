from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.personal_area.profile import withdraw_money
from loader import dp, bot
from utils.db_api.transactions import select_transactions_by_user_id
from utils.db_api.users_model import get_user_by_chat_id, get_count_referrals_by_chat_id


@dp.message_handler(Text(equals='👤 Мой аккаунт'), state='*')
async def process_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_info = await get_user_by_chat_id(message.from_user.id)

    referrals_count = await get_count_referrals_by_chat_id(chat_id=message.from_user.id)
    bot_name = await bot.get_me()
    all_day = datetime.now() - user_info.ts
    purchase_amount = sum(await select_transactions_by_user_id(message.from_user.id))

    text = f"""
<b>Мой профиль</b>

🆔 Ваш ID: {message.from_user.id}
🤖 Вы с нами с {user_info.ts.strftime("%d.%m.%Y")} ({all_day.days} дней)
💵 Сумма ваших покупок: {purchase_amount} рублей

<b>Партнерская программа</b>
Двухуровневая система: от 1-го уровня - личные  продажи и и от второго уровня - продажи партнёров. Первый уровень - 10%, второй 3%.

🤝 Приглашено: {referrals_count} рефералов
💰 Реферальный баланс: {user_info.balance} ₽
⤵️ Реферальная ссылка: https://t.me/{bot_name.username}?start=ref-{user_info.chat_id}
    """

    await message.answer(text, reply_markup=withdraw_money)
