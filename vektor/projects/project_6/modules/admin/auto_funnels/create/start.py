from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.inline import auto_funnels_list_data, auto_funnels_menu_data, create_auto_funnel_keyboard
from loader import dp
from states import CreateAutoFunnels


@dp.callback_query_handler(auto_funnels_list_data.filter(prefix='create'))
@dp.callback_query_handler(auto_funnels_menu_data.filter(prefix='create_new'))
async def process_creating_auto_funnels(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('Введите название воронки')
    await CreateAutoFunnels.get_name.set()
    await state.update_data({
        'name': None,  # Имя новой воронки
        'is_start_on_week': False,  # Если старт на определенный день недели
        'start_on_week': None,  # Если старт на определенный день недели
        'is_start_on_day_month': False,  # Если старт на определныый день месяца
        'start_on_day_month': None,  # Если старт на определныый день месяца
        'fast_start': False,  # Если быстрый старт на слудющий день
        'product': None,  # Продукт который продается в этой воронке
        'if_buy': None,  # Воронка если человек купил продукт
        'if_not_buy': None,  # Воронка если человек не купил продукт
        'created': False
    })
