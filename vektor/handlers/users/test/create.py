from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.admin.start import process_start
from handlers.users.projects.start import process_start_project
from keyboards.inline import start_data
from loader import dp
from utils.db_api.users_model import update_status_free_active, get_user_by_chat_id


@dp.callback_query_handler(start_data.filter(pr="create"))
async def create_handler(call: types.CallbackQuery, state: FSMContext):
    user = await get_user_by_chat_id(call.from_user.id)
    if user.trial_activate:
        await call.answer("Пробный период уже был активирован.", show_alert=True)
        await call.message.delete()
        return

    await call.answer("Пробный период активирован. Срок тестирования - 7 дней.")
    await update_status_free_active(call.from_user.id, True, True)
    await process_start_project(call,state)
