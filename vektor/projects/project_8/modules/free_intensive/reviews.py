from aiogram import types

from loader import bot, dp
from modules.BotKeyboards import free_intensive_data
from modules.DataBase import get_animation_by_name, get_audio_by_name, get_photo_by_name_tg_id


@dp.callback_query_handler(free_intensive_data.filter(filter="reviews"))
async def process_sending_images(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    media = types.MediaGroup()
    photo_1 = get_photo_by_name_tg_id("либидо 1")
    photo_2 = get_photo_by_name_tg_id("либидо 2")
    media.attach_photo(photo_1)
    media.attach_photo(photo_2)
    await bot.send_media_group(chat_id=call.from_user.id, media=media)


@dp.callback_query_handler(free_intensive_data.filter(filter="reviews_after_before"))
async def process_sending_images_before_after(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    media = types.MediaGroup()
    photo_1 = get_photo_by_name_tg_id("фото до-после 1")
    photo_2 = get_photo_by_name_tg_id("фото до-после 2")
    photo_3 = get_photo_by_name_tg_id("фото до-после 3")
    photo_4 = get_photo_by_name_tg_id("фото до-после 4")
    media.attach_photo(photo_1)
    media.attach_photo(photo_2)
    media.attach_photo(photo_3)
    media.attach_photo(photo_4)
    await bot.send_media_group(chat_id=call.from_user.id, media=media)
