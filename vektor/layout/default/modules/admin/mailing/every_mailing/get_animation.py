from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from .final import final_message
from states.every_mailing import EveryMailing


@dp.message_handler(Command('skip'), state=EveryMailing.get_animation)
async def skipping_get_animation(message: types.Message):
    await message.answer('Добавьте документ\n Пропустить => /skip')
    await EveryMailing.get_document.set()


@dp.message_handler(state=EveryMailing.get_animation, content_types=types.ContentTypes.ANIMATION)
async def process_get_animation(message: types.Message, state: FSMContext):
    animation = message.animation.file_id
    await state.update_data({'animation': animation})
    data = await state.get_data()
    await final_message(data, message.from_user.id)
    await EveryMailing.final.set()