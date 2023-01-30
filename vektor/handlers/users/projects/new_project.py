from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.list_projects import list_project_data
from loader import dp
from states.create_project import CreateProject
from utils.db_api.users_model import get_user_by_chat_id


@dp.callback_query_handler(list_project_data.filter(pr='new'))
async def process_new_project(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text('Введите название проекта')
    await CreateProject.name.set()
    await state.update_data(data={
        'name': None
    })
