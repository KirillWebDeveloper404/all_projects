from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.create_project import CreateProject


@dp.message_handler(state=CreateProject.name)
async def process_get(message: types.Message, state: FSMContext):
    await state.update_data(data={
        'name': message.text
    })
    await message.answer('Отправьте токен бота')
    await CreateProject.token.set()