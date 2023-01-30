from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedPhoto

from filters import IsAdmin
from keyboard.inline.users.manage_users import get_manage_users_kb
from loader import dp
from modules.BotKeyboards import generate_link_keyboard
from modules.DataBase import get_all_users_by_phone, is_admin, get_not_deleted_products_search


@dp.inline_handler(text='')
async def empty_query(query: types.InlineQuery):
    print('Пустой запрос')
    await query.answer(results=[
        InlineQueryResultArticle(
            id='unknown',
            title='Введите какой-то запрос',
            input_message_content=InputTextMessageContent(
                message_text='Не обязательно жать на эту кнопку'
            )
        )
    ])


@dp.inline_handler(IsAdmin(), Text(startswith='номер:'))
async def process_inline_search(inline: types.InlineQuery):
    results = []
    query = inline.query
    phone = query.replace('номер:', '')
    users = get_all_users_by_phone(phone)

    for user in users:
        title = f'{user.name} - {user.phone_number}'
        text = f'Пользователь: {user.name} \n' \
               f'Телефон: {user.phone_number} \n' \
               f'Зарегистрировался: {user.ts}\n' \
               f'Стадия: {user.stage}'
        input_message_content = InputTextMessageContent(
            message_text=text
        )
        keyboard = await get_manage_users_kb(user.id)
        result = InlineQueryResultArticle(
            id=f'user-{user.id}',
            title=title,
            input_message_content=input_message_content,
            description=text,
            reply_markup=keyboard
        )
        results.append(result)

    await inline.answer(
        results=results
    )
