from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, generate_get_document_keyboard, msg_document_af_data
from loader import dp
from states import CreateMessageAF
from .get_main_text import send_main_text


@dp.callback_query_handler(create_message_af.filter(prefix='document'), state=CreateMessageAF.choice)
async def process_add_document_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_document_keyboard(data)
    await call.message.delete()
    if data['document']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Отправьте файл:', reply_markup=keyboard)
        await CreateMessageAF.get_document.set()


@dp.message_handler(state=CreateMessageAF.get_document, content_types=types.ContentTypes.DOCUMENT)
async def process_get_document_message(message: types.Message, state: FSMContext):
    document = message.document.file_id
    await state.update_data(data={
        'document': document
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_document, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_document_keyboard(data)
    await message.answer('Вы отправили не тот файл, отправьте мне нужный файл.', reply_markup=keyboard)


@dp.callback_query_handler(msg_document_af_data.filter(prefix='change_document'), state=CreateMessageAF.choice)
async def process_change_gif_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'document': None
    })
    data = await state.get_data()
    keyboard = await generate_get_document_keyboard(data)
    await call.message.edit_text('Отправьте файл:', reply_markup=keyboard)
    await CreateMessageAF.get_document.set()
