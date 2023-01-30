from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from modules.BotKeyboards import every_mailing
from states.every_mailing import EveryMailing


@dp.callback_query_handler(state=EveryMailing.init)
async def get_data_mailing(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    await state.update_data({'data': call.data})
    await call.message.edit_text('Выберете метод:', reply_markup=every_mailing)
    await EveryMailing.get_type.set()


