from aiogram import types

from keyboards.inline.admin.back_statistic import back_statistic
from keyboards.inline.admin.start import admin_data
from loader import dp
from utils.db_api.users_model import get_count_users, get_count_user_free_active, get_count_is_payment


@dp.callback_query_handler(admin_data.filter(pr="statistics"))
async def statistic_handler(call: types.CallbackQuery):
    count_users = await get_count_users()
    count_free_active = await get_count_user_free_active(True)
    count_is_payment = await get_count_is_payment(True)

    text = f"""Общее количество 
Всего пользователей: {count_users}
На пробном периоде: {count_free_active}
На платной подписке: {count_is_payment}
    """
    await call.message.edit_text(text=f"<b>Статистика</b>\n{text}", reply_markup=back_statistic)