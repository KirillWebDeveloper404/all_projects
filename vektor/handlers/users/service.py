from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.service_keyboard import generate_service_keyboard
from loader import dp


@dp.message_handler(Text(equals='⚡️О сервисе'), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = 'Vector Education — сервис для образовательных проектов в телеграмм.\n\n' \
           'Здесь есть все для монетизации знаний.'
    keyboard = await generate_service_keyboard()
    await message.answer(text, reply_markup=keyboard)

