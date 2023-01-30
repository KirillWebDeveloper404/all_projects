from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states.every_mailing import EveryMailing
from .final import final_message


@dp.message_handler(Command('skip'), state=EveryMailing.get_photo)
async def skipping_get_photo(message: types.Message):
    await message.answer('Добавьте анимацию\n Пропустить => /skip')
    await EveryMailing.get_animation.set()


@dp.message_handler(state=EveryMailing.get_photo, content_types=types.ContentTypes.PHOTO)
async def process_get_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data({'photo': photo})
    data = await state.get_data()
    await final_message(data, message.from_user.id)
    await EveryMailing.final.set()
