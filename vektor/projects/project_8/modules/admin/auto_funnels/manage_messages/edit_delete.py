from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import delete_time_kb, delete_time_data
from keyboard.inline.edit.delete import generate_edit_delete_keyboard, edit_delete
from keyboard.inline.edit.edit_message import edit_message_kb_data
from loader import dp
from states import EditMessages
from utils.functions.edit_messages_msg import get_text_edit_messages


@dp.callback_query_handler(edit_message_kb_data.filter(prefix='delete'), state=EditMessages.start)
async def process_delete_get(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    await call.message.delete()
    if data['delete_hour'] or data['delete_day'] or data['delete_minute'] or data['delete_second']:
        keyboard = await generate_edit_delete_keyboard(data=data)
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        text = 'Выберете через сколько сообщение удалится:'
        await call.message.answer(text, reply_markup=delete_time_kb)
        await EditMessages.delete.set()


@dp.callback_query_handler(delete_time_data.filter(), state=EditMessages.delete)
async def get_delete_hour(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=1)
    day = int(callback_data.get('day'))
    hour = int(callback_data.get('hour'))
    minute = int(callback_data.get('minute'))
    second = int(callback_data.get('second'))
    await state.update_data(data={
        'delete_day': day,
        'delete_hour': hour,
        'delete_minute': minute,
        'delete_second': second,
    })
    data = await state.get_data()
    await EditMessages.start.set()
    await get_text_edit_messages(data, call.message, delete=True)


@dp.callback_query_handler(edit_delete.filter(prefix='change'), state=EditMessages.start)
async def process_change_delete_hour(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'delete_day': None,
        'delete_hour': None,
        'delete_minute': None,
        'delete_second': None,
    })

    text = 'Выберете через сколько сообщение удалится:'
    await call.message.edit_text(text, reply_markup=delete_time_kb)
    await EditMessages.delete.set()
