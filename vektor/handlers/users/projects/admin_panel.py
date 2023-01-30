from aiogram import types

# from admin_panel.modules.admin.start import start_admin
from keyboards.inline.manage_project import manage_project_data, get_manage_project_kb
from loader import dp


@dp.callback_query_handler(manage_project_data.filter(pr='admin-p'))
async def process_on_project(call: types.CallbackQuery, callback_data: dict):
    project_id = int(callback_data.get('pj_id'))
    await call.answer("В разработке", show_alert=True)
    # await start_admin(call)