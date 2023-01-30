from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import DateMailing

@dp.message_handler(state=DateMailing.get_text)
async def process_get_text(message: types.Message, state=FSMContext):
    message_text = message.text
    await state.update_data({'message_text': message_text})
    await message.answer('Добавитть ссылку, пропустить => /skip')
    await DateMailing.get_link.set()