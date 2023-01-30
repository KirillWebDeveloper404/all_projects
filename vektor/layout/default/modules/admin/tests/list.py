from aiogram import types

from keyboard.inline.tests.list import list_tests_data, generate_list_tests_keyboard
from keyboard.inline.tests.main import test_main_data, test_main
from keyboard.inline.tests.manage_question import get_manage_question_keyboard
from loader import dp
from modules.BotKeyboards import admin_main
from modules.DataBase import get_answers_question


@dp.callback_query_handler(test_main_data.filter(prefix='list'))
async def get_list_tests(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    text = 'Выберете квиз'
    keyboard = await generate_list_tests_keyboard()

    await call.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(list_tests_data.filter(id='back'))
async def back_list_tests(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Квизы', reply_markup=test_main)


@dp.callback_query_handler(test_main_data.filter(prefix='back'))
async def back_list_tests(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Управление', reply_markup=admin_main)
