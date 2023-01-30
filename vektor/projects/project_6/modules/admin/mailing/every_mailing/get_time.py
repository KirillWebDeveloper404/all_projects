from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.every_mailing import EveryMailing


@dp.message_handler(state=EveryMailing.get_time)
async def process_get_time(message: types.Message, state=FSMContext):
    time = message.text.strip().split(':')
    hour = int(time[0])
    minute = int(time[1])
    await state.update_data({'hour': hour, 'minute': minute})
    await message.answer('Отправьте сообщение рассылки')
    await EveryMailing.get_text.set()
