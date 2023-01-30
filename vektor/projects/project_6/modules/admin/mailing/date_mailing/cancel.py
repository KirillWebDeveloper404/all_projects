from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import DateMailing


@dp.message_handler(Command('cancel'), state=DateMailing)
async def process_cancel_create_job(message: types.Message, state: FSMContext):
    await message.answer('Создание рассылки отменено')
    await state.finish()
