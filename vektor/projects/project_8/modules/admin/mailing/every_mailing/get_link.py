from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states.every_mailing import EveryMailing


@dp.message_handler(Command('skip'), state=EveryMailing.get_link)
async def skipping_get_link(message: types.Message):
    await message.answer('Добавьте фото\n Пропустить => /skip')
    await EveryMailing.get_photo.set()


@dp.message_handler(state=EveryMailing.get_link)
async def process_get_link(message: types.Message, state: FSMContext):
    link = message.text.strip()
    await state.update_data({'link': link})
    await message.answer(
        'Добавьте текст ссылки(Если не добавить будет стандартный текст "Ссылка")\n Пропустить => /skip')
    await EveryMailing.get_text_link.set()
