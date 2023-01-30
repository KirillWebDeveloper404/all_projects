from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import when_start, create_af_data, create_auto_funnel_keyboard
from loader import dp
from .final_message import get_final_message
from states import CreateAutoFunnels
from utils.functions import transliteration


@dp.callback_query_handler(create_af_data.filter(prefix='name'), state=CreateAutoFunnels.choice)
async def process_send_get_name(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте новое название воронки')
    await CreateAutoFunnels.get_name.set()


@dp.message_handler(state=CreateAutoFunnels.get_name)
async def process_get_name(message: types.Message, state: FSMContext):
    name = await transliteration(message.text)
    if name == 'stop':
        await message.answer('Поздравляю, вы нашли единственное исключение в имени, такое имя нельзя создавать, '
                             'прошу вас напишите любое другое имя кроме этого)')
        return
    await state.update_data({
        'name': name
    })
    data = await state.get_data()
    if data['created']:
        text = await get_final_message(data)
        keyboard = await create_auto_funnel_keyboard(data)
        await message.answer(text, reply_markup=keyboard)
        await CreateAutoFunnels.choice.set()
    else:
        await message.answer('Выберете условия старта воронки', reply_markup=when_start)
        await CreateAutoFunnels.get_when_start.set()


