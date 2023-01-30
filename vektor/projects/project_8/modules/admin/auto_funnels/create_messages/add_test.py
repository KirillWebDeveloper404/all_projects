from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_af
from keyboard.inline.create_message_af.get_msg_test import generate_get_test_keyboard, msg_test_af_data_id, \
    msg_test_af_data
from loader import dp
from modules.admin.auto_funnels.create_messages.get_main_text import send_main_text
from states import CreateMessageAF


@dp.callback_query_handler(create_message_af.filter(prefix='test'), state=CreateMessageAF.choice)
async def process_get_test_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    keyboard = await generate_get_test_keyboard(data)
    await call.message.delete()
    if data['test']:
        await call.message.answer('Выберете:', reply_markup=keyboard)
    else:
        await call.message.answer('Выберете вопрос:', reply_markup=keyboard)
        await CreateMessageAF.get_test.set()


@dp.callback_query_handler(msg_test_af_data_id.filter(), state=CreateMessageAF.get_test)
async def process_get_test_message(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    question_id = int(callback_data.get('id'))
    await call.answer(cache_time=1)
    await state.update_data(data={
        'test': question_id
    })
    data = await state.get_data()
    await CreateMessageAF.choice.set()
    await send_main_text(data=data, message=call.message, delete=True)



@dp.callback_query_handler(msg_test_af_data.filter(prefix='change_test'), state=CreateMessageAF.choice)
async def process_get_test_message(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data(data={
        'test': None
    })
    data = await state.get_data()
    keyboard = await generate_get_test_keyboard(data)
    await call.message.delete()
    await call.message.answer('Выберете вопрос:', reply_markup=keyboard)
    await CreateMessageAF.get_test.set()