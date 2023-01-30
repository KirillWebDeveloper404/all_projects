from aiogram.dispatcher import FSMContext

from keyboard.inline import create_message_keyboard, auto_funnels_manage_messages_data
from keyboard.inline.create_message_af import create_message_af
from keyboard.inline.create_message_af.all_data import create_message_funnel
from keyboard.inline.manage_message.all_datas import create_new_message_af_ff
from loader import dp
from aiogram import types

from modules.DataBase import get_auto_funnel_by_id
from .save_message import save_message
from states import CreateMessageAF


@dp.callback_query_handler(create_new_message_af_ff.filter())
@dp.callback_query_handler(auto_funnels_manage_messages_data.filter(prefix='new'))
@dp.callback_query_handler(create_message_funnel.filter(), state='*')
async def process_add_message_starting(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    try:
        msg_type = callback_data.get('msg_type')
    except:
        msg_type = None

    try:
        funnel_id = callback_data.get('funnel_id')
    except:
        funnel_id = None
    try:
        save = callback_data.get('save')
    except:
        save = None

    try:
        edit = callback_data.get('edit')
    except:
        edit = False

    if edit:
        if edit == 'yes':
            edit = True

    if save:
        if save == 'Yes':
            data = await state.get_data()
            await save_message(data)
        if save == 'one':
            is_add_exit = True

    await CreateMessageAF.choice.set()
    await call.answer(cache_time=1)
    await state.update_data(data={
        'photo': None,
        'gif': None,
        'video': None,
        'audio': None,
        'voice': None,
        'video_note': None,
        'text': None,
        'test': None,
        'document': None,
        'day': None,
        'hour': None,
        'minute': None,
        'interval_msg': None,
        'interval_hour': None,
        'interval_minute': None,
        'interval_second': None,
        'interval_day': None,
        'delete_second': None,
        'delete_minute': None,
        'delete_hour': None,
        'delete_day': None,
        'link': None,
        'text_link': None,
        'is_add_exit': edit
    })
    if msg_type and funnel_id:
        is_fast_start = get_auto_funnel_by_id(funnel_id).fast_start
        await state.update_data(data={
            'type': msg_type,
            'funnel_id': funnel_id,
            'is_fast_start': is_fast_start
        })
    data = await state.get_data()
    text = ''
    if data['type'] == 'first':
        text += 'Добавьте первое сообщение'
    if data['type'] == 'system':
        text += 'Добавьте системное сообщение'
    if data['type'] == 'content':
        text += 'Добавьте сообщение воронки'

    keyboard = await create_message_keyboard(data=data)
    await call.message.delete()
    await call.message.answer(text=text, reply_markup=keyboard)
