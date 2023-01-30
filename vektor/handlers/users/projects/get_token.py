from unittest.mock import call

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ValidationError

from keyboards.inline.add_rates import get_rates_list_add_to_create
from keyboards.inline.manage_project import get_manage_project_kb
from loader import dp, bots_manager
from states.create_project import CreateProject
from utils.db_api.projects_model import create_project, token_exists
from utils.db_api.rates_model import get_all_rates, get_rate_by_id
from utils.db_api.users_model import get_user_by_chat_id


@dp.message_handler(state=CreateProject.token)
async def process_get(message: types.Message, state: FSMContext):
    token = message.text
    await state.update_data(data={
        'token': token
    })
    try:
        Bot(token=token)
    except ValidationError:
        await message.answer('Не правильный токен бота, попробуйте еще раз!')
        return
    is_token_exists = await token_exists(token=token)
    if len(is_token_exists) > 0:
        await message.answer('Этот токен уже зарегистрирован')
        return
    data = await state.get_data()

    user = await get_user_by_chat_id(message.from_user.id)
    rate = await get_rate_by_id(1)

    if user.free_active:
        project = await create_project(
            token=data['token'],
            chat_id=message.from_user.id,
            name=data['name'],
            rate=rate.id)

        # print(project)
        await message.answer("Создаем проект. Ожидайте.")
        await bots_manager.add_bot(int(project.id), data['token'], path_layout='layout/default', admin=message.from_user.id)
        await bots_manager.__on_status__(project.id)
        text = await bots_manager.get_info_bot(project.id)
        keyboard = await get_manage_project_kb(project.id)
        await message.answer(text, reply_markup=keyboard)

        await state.finish()
        return

    rates = await get_all_rates()
    text = 'Выберете тариф\n\n'
    for rate in rates:
        if rate.id == 1:
            continue
        text += f'Тариф: {rate.name}\n' \
                f'{rate.desc}\n\n'

    keyboard = await get_rates_list_add_to_create()
    await message.answer(text, reply_markup=keyboard)
    await CreateProject.rate.set()

