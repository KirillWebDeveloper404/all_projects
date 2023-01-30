from aiogram import types

from keyboards.inline.list_projects import list_project_data, generate_list_project
from keyboards.inline.manage_project import get_manage_project_kb, manage_project_data
from loader import dp, bots_manager


@dp.callback_query_handler(list_project_data.filter(pr='project'))
async def process_new_project(call: types.CallbackQuery, callback_data: dict):
    # await call.answer(cache_time=1)
    # print(callback_data)
    project_id = int(callback_data.get('project_id'))
    text = await bots_manager.get_info_bot(project=project_id)
    keyboard = await get_manage_project_kb(project_id)
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(manage_project_data.filter(pr='back'))
async def process_on_project(call: types.CallbackQuery):
    keyboard = await generate_list_project(chat_id=call.from_user.id)
    await call.message.edit_text('Список проектов', reply_markup=keyboard)
