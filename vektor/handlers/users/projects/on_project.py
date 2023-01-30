from aiogram import types

from keyboards.inline.manage_project import manage_project_data, get_manage_project_kb
from loader import dp, bots_manager
from utils.db_api.projects_model import get_project_by_user_chat_id, get_project_by_id
from utils.db_api.users_model import get_user_by_chat_id


@dp.callback_query_handler(manage_project_data.filter(pr='on'))
async def process_on_project(call: types.CallbackQuery, callback_data: dict):
    project_id = int(callback_data.get('pj_id'))
    project = await get_project_by_id(project_id)
    user = await get_user_by_chat_id(call.from_user.id)
    if user.free_active or project.is_payment:
        await call.answer(cache_time=1)
        await bots_manager.__on_status__(project=project_id)
        text = await bots_manager.get_info_bot(project=project_id)
        keyboard = await get_manage_project_kb(project_id)
        await call.message.edit_text(text, reply_markup=keyboard)
    else:
        await call.answer("Вы не можете включить бота из-за неуплаты или пробный период закончился.", show_alert=True)

