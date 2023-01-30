from aiogram import types

from keyboards.inline.list_projects import generate_list_project
from keyboards.inline.manage_project import manage_project_data, get_manage_project_kb
from loader import dp, bots_manager
from utils.db_api.projects_model import delete_project_by_id


@dp.callback_query_handler(manage_project_data.filter(pr='delete'))
async def process_on_project(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    project_id = int(callback_data.get('pj_id'))
    await bots_manager.__delete_project__(project=project_id)
    await delete_project_by_id(project_id)
    keyboard = await generate_list_project(chat_id=call.from_user.id)
    await call.message.edit_text('Список проектов', reply_markup=keyboard)