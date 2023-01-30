from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin.service_keyboard import service_data, generate_service_keyboard_admin
from loader import dp
from states.setting_change import ChangeSettings
from utils.db_api.settings_model import change_settings, get_settings


@dp.callback_query_handler(service_data.filter(pr='chat'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте ссылку на чат')
    await ChangeSettings.chat.set()


@dp.message_handler(state=ChangeSettings.chat)
async def process_get_chat(message: types.Message, state: FSMContext):
    await state.finish()
    await change_settings(chat=message.text)
    settings = await get_settings()

    text = f'Сайт - {settings.site}\n' \
           f'Канал - {settings.channel}\n' \
           f'Поддержка - {settings.helper}\n' \
           f'Чат - {settings.chat}'
    keyboard = await generate_service_keyboard_admin()
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(service_data.filter(pr='helper'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте ссылку')
    await ChangeSettings.helper.set()


@dp.message_handler(state=ChangeSettings.helper)
async def process_get_help(message: types.Message, state: FSMContext):
    await state.finish()
    await change_settings(helper=message.text)
    settings = await get_settings()

    text = f'Сайт - {settings.site}\n' \
           f'Канал - {settings.channel}\n' \
           f'Поддержка - {settings.helper}\n' \
           f'Чат - {settings.chat}'
    keyboard = await generate_service_keyboard_admin()
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(service_data.filter(pr='channel'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте ссылку')
    await ChangeSettings.channel.set()


@dp.message_handler(state=ChangeSettings.channel)
async def process_get_channel(message: types.Message, state: FSMContext):
    await state.finish()
    await change_settings(channel=message.text)
    settings = await get_settings()

    text = f'Сайт - {settings.site}\n' \
           f'Канал - {settings.channel}\n' \
           f'Поддержка - {settings.helper}\n' \
           f'Чат - {settings.chat}'
    keyboard = await generate_service_keyboard_admin()
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(service_data.filter(pr='site'))
async def process_back(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Отправьте ссылку')
    await ChangeSettings.site.set()


@dp.message_handler(state=ChangeSettings.site)
async def process_get_channel(message: types.Message, state: FSMContext):
    await state.finish()
    await change_settings(site=message.text)
    settings = await get_settings()

    text = f'Сайт - {settings.site}\n' \
           f'Канал - {settings.channel}\n' \
           f'Поддержка - {settings.helper}\n' \
           f'Чат - {settings.chat}'
    keyboard = await generate_service_keyboard_admin()
    await message.answer(text, reply_markup=keyboard)
