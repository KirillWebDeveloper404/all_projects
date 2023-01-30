from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af, generate_get_text_keyboard, msg_text_af_data, \
    generate_get_photo_keyboard, msg_photo_af_data
from loader import dp
from .get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(create_message_af.filter(prefix='photo'), state=CreateMessageAF.choice)
async def process_add_photo_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_photo_keyboard(data)
    await call.message.delete()
    if data['photo']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Отправьте изображение:', reply_markup=keyboard)
        await CreateMessageAF.get_photo.set()


@dp.message_handler(state=CreateMessageAF.get_photo, content_types=types.ContentTypes.PHOTO)
async def process_get_photo_message(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(data={
        'photo': photo
    })
    data = await state.get_data()
    await send_main_text(data, message)
    await CreateMessageAF.choice.set()


@dp.message_handler(state=CreateMessageAF.get_photo, content_types=types.ContentTypes.ANY)
async def process_get_audio_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_photo_keyboard(data)
    await message.answer('Вы отправили не тот файл, отправьте мне нужный файл.', reply_markup=keyboard)



@dp.callback_query_handler(msg_photo_af_data.filter(prefix='change_photo'), state=CreateMessageAF.choice)
async def process_change_photo_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'photo': None
    })
    data = await state.get_data()
    keyboard = await generate_get_photo_keyboard(data)
    await call.message.edit_text('Отправьте изображение:', reply_markup=keyboard)
    await CreateMessageAF.get_photo.set()
