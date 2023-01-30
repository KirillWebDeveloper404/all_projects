import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils.exceptions import BotBlocked, ChatNotFound, UserDeactivated
from peewee import DoesNotExist

from loader import dp, bot

from modules.BotKeyboards import admin_mailing_data, mailing_keyboard
from modules.Methods import is_url_valid
from utils.functions.get_users_segment import get_users


class MailingStates(StatesGroup):
    init = State()
    waiting_for_description = State()
    waiting_for_photo_or_gif = State()
    waiting_for_document = State()
    waiting_for_link = State()


@dp.callback_query_handler(admin_mailing_data.filter(prefix='back'), state='*')
async def process_back_to_mailing(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await call.message.edit_text('Рассылка', reply_markup=mailing_keyboard)


@dp.callback_query_handler(lambda c: c.data, state=MailingStates.init)
async def initialize_mailing(callback: types.CallbackQuery, state: FSMContext):
    recipients = list()
    segment = list()

    segment = await get_users(data=callback.data)
    for user in segment:
        recipients.append(user.tg_id)
    await state.update_data(recipients=recipients)

    await bot.send_message(callback.from_user.id, "Отправьте текст для поста")
    await MailingStates.waiting_for_description.set()


@dp.message_handler(state=MailingStates.waiting_for_description, content_types=types.ContentType.TEXT)
async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await bot.send_message(message.from_user.id, "Отправьте фото или gif, или же команду /skip")
    await MailingStates.waiting_for_photo_or_gif.set()


@dp.message_handler(
    state=MailingStates.waiting_for_photo_or_gif,
    content_types=[types.ContentType.PHOTO, types.ContentType.ANIMATION, types.ContentType.TEXT],
)
async def get_photo(message: types.Message, state):
    if message.content_type == types.ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        await state.update_data(photo=file_id)
    elif message.content_type == types.ContentType.ANIMATION:
        file_id = message.animation.file_id
        await state.update_data(animation=file_id)
    elif message.content_type == types.ContentType.TEXT:
        if "skip" not in message.text:
            await bot.send_message(
                message.from_user.id, "Отправьте фото или gif, или же команду /skip",
            )
            return

    await bot.send_message(
        message.from_user.id, "Отправьте документ или нажмите /skip",
    )
    await MailingStates.waiting_for_document.set()


@dp.message_handler(
    state=MailingStates.waiting_for_document, content_types=[types.ContentType.DOCUMENT, types.ContentType.TEXT]
)
async def get_photo(message: types.Message, state):
    if message.content_type == types.ContentType.DOCUMENT:
        file_id = message.document.file_id
        await state.update_data(document=file_id)
    elif message.content_type == types.ContentType.TEXT:
        if "skip" not in message.text:
            await bot.send_message(
                message.from_user.id, "Отправьте документ или команду /skip",
            )
            return

    await bot.send_message(
        message.from_user.id, "Отправьте ссылку или нажмите /skip",
    )
    await MailingStates.waiting_for_link.set()


@dp.message_handler(state=MailingStates.waiting_for_link, content_types=types.ContentType.TEXT)
async def get_link(message, state):
    url = None
    if "skip" not in message.text:
        if not is_url_valid(message.text):
            await message.reply(
                "Пожалуйста, введите правильную ссылку. Например: https://us04web.zoom.us/j/123?pwd=456"
            )
            return
        url = message.text
    data = await state.get_data()

    recipients = data["recipients"]
    description = data["description"]
    photo = data.get("photo", None)
    animation = data.get("animation", None)
    document = data.get("document", None)

    failed = 0
    for tg_id in recipients:
        try:
            if photo:
                await bot.send_photo(tg_id, photo, disable_notification=True)
            elif animation:
                await bot.send_animation(tg_id, animation, disable_notification=True)
            if url:
                await bot.send_message(
                    tg_id,
                    description,
                    reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton("Подробнее", url=url)),
                )
            else:
                await bot.send_message(tg_id, description)
            if document:
                await bot.send_document(tg_id, document, disable_notification=True)

        except (ChatNotFound, BotBlocked, UserDeactivated):
            logging.warning(f"Impossible to notify {tg_id}")
            failed += 1
    await bot.send_message(
        message.from_user.id,
        f"Рассылка закончена\n"
        f"Из *{len(recipients)}* пользователей в рассылке:\n"
        f"- *{len(recipients) - failed}* пользователям отправлено успешно,\n"
        f"- *{failed}* пользователям невозможно отправить",
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.finish()
