from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from modules.admin.mailing.date_mailing.final import final_message
from states import DateMailing


@dp.message_handler(Command('skip'), state=DateMailing.get_document)
async def skipping_get_animation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await final_message(data, message.from_user.id)
    await DateMailing.final.set()


@dp.message_handler(state=DateMailing.get_document, content_types=types.ContentTypes.DOCUMENT)
async def process_get_animation(message: types.Message, state: FSMContext):
    document = message.document.file_id
    await state.update_data({'document': document})
    data = await state.get_data()
    await final_message(data, message.from_user.id)
    await DateMailing.final.set()