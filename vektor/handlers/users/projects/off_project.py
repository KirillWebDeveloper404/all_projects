from aiogram import types

from keyboards.inline.manage_project import manage_project_data, get_manage_project_kb
from loader import dp, bots_manager


@dp.callback_query_handler(manage_project_data.filter(pr='off'))
async def process_on_project(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    project_id = int(callback_data.get('pj_id'))
    await bots_manager.__off_status__(project=project_id)
    text = await bots_manager.get_info_bot(project=project_id)
    keyboard = await get_manage_project_kb(project_id)
    await call.message.edit_text(text, reply_markup=keyboard)
