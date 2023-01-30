from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline.edit.edit_message import edit_message_kb_data
from keyboard.inline.edit.edit_test import generate_get_test_keyboard, edit_test_af_data_id, edit_test_af_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='test'), state=EditMessages.start)
async def process_start_edit(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    keyboard = await generate_get_test_keyboard(data)
    await call.message.delete()
    if not keyboard:
        await call.answer(text='У вас еще нет квизов!', show_alert=True, cache_time=1)

    if data['test']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Выберете вопрос:', reply_markup=keyboard)
        await EditMessages.test.set()
    await call.answer(cache_time=1)


@dp.callback_query_handler(edit_test_af_data_id.filter(), state=EditMessages.test)
async def process_get_test_message(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    question_id = int(callback_data.get('id'))
    await call.answer(cache_time=1)
    await state.update_data(data={
        'test': question_id
    })
    data = await state.get_data()
    await EditMessages.start.set()
    await get_text_edit_messages(data, call.message, delete=True)


@dp.callback_query_handler(edit_test_af_data.filter(prefix='change'), state=EditMessages.start)
async def process_get_test_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'test': None
    })
    data = await state.get_data()
    keyboard = await generate_get_test_keyboard(data)
    await call.message.delete()
    await call.message.answer('Выберете вопрос:', reply_markup=keyboard)
    await EditMessages.test.set()
