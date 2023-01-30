from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import DateMailing


@dp.message_handler(state=DateMailing.get_time)
async def process_get_time(message: types.Message, state=FSMContext):
    time = message.text.strip().split(':')
    if time[0] == '00':
        hour = 0
    elif time[0].startswith('0'):
        hour = int(time[0].replace('0', ''))
    else:
        hour = int(time[0])
    if hour >= 24 or hour < 0:
        await message.answer('Вы не правильно ввели время, ввведите еще раз')
        return

    if time[1] == '00':
        minute = 0
    elif time[1].startswith('0'):
        minute = int(time[1].replace('0', ''))
    else:
        minute = int(time[1])

    if minute >= 60 or minute < 0:
        await message.answer('Вы не правильно ввели время, ввведите еще раз')
        return
    await state.update_data({'hour': hour, 'minute': minute})
    await message.answer('Отправьте сообщение рассылки')
    await DateMailing.get_text.set()
