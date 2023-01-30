from aiogram import types

from keyboards.inline.admin.service_keyboard import service_data, \
    generate_service_keyboard_admin
from keyboards.inline.admin.start import admin_data, admin_start
from loader import dp
from utils.db_api.settings_model import get_settings


@dp.callback_query_handler(admin_data.filter(pr='service'))
async def process_start(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    settings = await get_settings()

    text = f'Сайт - {settings.site}\n' \
           f'Канал - {settings.channel}\n' \
           f'Поддержка - {settings.helper}\n' \
           f'Чат - {settings.chat}'
    keyboard = await generate_service_keyboard_admin()
    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(service_data.filter(pr='back'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Админ-панель', reply_markup=admin_start)
