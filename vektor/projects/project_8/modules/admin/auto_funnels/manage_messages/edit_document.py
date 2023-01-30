from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_document import generate_get_document_keyboard, edit_document_msg_data
from keyboard.inline.edit.edit_message import edit_message_kb_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='document'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    keyboard = await generate_get_document_keyboard(data)
    if data['document']:
        text = 'Выберете:'
    else:
        text = 'Отправьте документ'
        await EditMessages.document.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.document, content_types=types.ContentTypes.DOCUMENT)
async def process_get(message: types.Message, state: FSMContext):
    document = message.document.file_id
    await state.update_data(data={
        'document': document
    })
    data = await state.get_data()
    await get_text_edit_messages(data, message)
    await EditMessages.start.set()


@dp.callback_query_handler(edit_document_msg_data.filter(prefix='change'), state=EditMessages.start)
async def process_change(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'document': None
    })
    text = 'Отправьте документ'
    data = await state.get_data()
    keyboard = await generate_get_document_keyboard(data)
    await EditMessages.document.set()
    await call.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state=EditMessages.document, content_types=types.ContentTypes.ANY)
async def process_error_file(message: types.Message):
    await message.answer('Вы отправили не тот тип файла')
