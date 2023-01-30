from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from keyboards.inline.list_projects import generate_list_project
from loader import dp
from states.create_project import CreateProject


@dp.message_handler(Text(equals='📌 Проекты'), state='*')
async def process_start_project(message: types.Message or types.CallbackQuery, state: FSMContext):
    await state.finish()
    keyboard = await generate_list_project(chat_id=message.from_user.id)
    await message.bot.send_message(message.from_user.id, 'Список проектов', reply_markup=keyboard)

