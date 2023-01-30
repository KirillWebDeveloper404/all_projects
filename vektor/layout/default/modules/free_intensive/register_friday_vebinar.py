from aiogram import types

from loader import dp
from modules.BotKeyboards import friday_vebinar_data
from modules.DataBase import register_user_friday_vebinar


@dp.callback_query_handler(friday_vebinar_data.filter())
async def process_register_users_friday_vebinar(call: types.CallbackQuery, callback_data: dict):
    time = callback_data.get('prefix')
    await call.answer(cache_time=1)
    register_user_friday_vebinar(call.from_user.id, time)
    await call.message.edit_caption(f'Вы успешно зарегистрированы на пятничный вебинар.\n'
                                    f'Завтра за час до начала пришлем вам напоминание и ссылку.')
