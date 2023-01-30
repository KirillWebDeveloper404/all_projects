from aiogram import types

from keyboard.inline import create_message_keyboard
from loader import bot
from modules.DataBase import get_message_af_by_id
from utils.functions import has_text_youtube_link


async def get_main_text(data) -> str:
    text = ''
    type_message = data['type']
    day = data['day']
    hour = data['hour']
    minute = data['minute']
    msg_text = data['text']
    interval_msg = data['interval_msg']
    delete_day = data['delete_day']
    delete_minute = data['delete_minute']
    delete_second = data['delete_second']
    delete_hour = data['delete_hour']
    link = data['link']
    funnel_id = data['funnel_id']

    if funnel_id:
        pass

    if type_message == 'first':
        text += 'Тип сообщения: первое\n'
    if type_message == 'system':
        text += 'Тип сообщения: системное\n'
    if type_message == 'content':
        text += 'Тип сообщения: контент\n'

    if day and (minute or minute == 0) and (hour == 0 or hour):
        text += f'Отправка: на {day} день в {hour}:{minute}\n'

    if interval_msg:
        interval_hour = data['interval_hour']
        interval_minute = data['interval_minute']
        interval_second= data['interval_second']
        interval_day = data['interval_day']
        interval_msg = get_message_af_by_id(interval_msg)
        if interval_msg.is_first:
            text += f'Сообщение будет отправлено после первого через ' \
                    f'через {interval_day} дней ' \
                    f'{interval_hour} часов ' \
                    f'{interval_minute} минут ' \
                    f'{interval_second} секунд\n\n'
        else:
            text += f'Сообщение будет отправлено после сообщения "{interval_msg.day} в {interval_msg.hour}:' \
                    f'{interval_msg.minute}" через {interval_day} дней ' \
                    f'{interval_hour} часов ' \
                    f'{interval_minute} минут ' \
                    f'{interval_second} секунд\n\n'

    if delete_hour or delete_day or delete_minute or delete_second:
        if delete_hour:
            text += f'Удаление: через {delete_hour} часов\n'
        elif delete_day:
            text += f'Удаление: через {delete_day} дня\n'
        elif delete_minute:
            text += f'Удаление: через {delete_minute} минут\n'
        elif delete_second:
            text += f'Удаление: через {delete_second} секунд\n'

    else:
        text += f'Удаление: отсутствует\n'

    if link:
        text_link = data['text_link']
        if text_link:
            text += f'Будет добавлена кнопка с ссылкой {link}, и надписью {text_link}\n'
        else:
            text += f'Будет добавлена кнопка с ссылкой {link}, и надписью "подробнее"\n'
    if msg_text:
        text += f'\nСообщение:\n{msg_text}'

    return text


async def send_main_text(data, message: types.Message, delete=False):
    photo = data['photo']
    gif = data['gif']
    video = data['video']
    video_note = data['video_note']
    audio = data['audio']
    voice = data['voice']
    document = data['document']
    text = await get_main_text(data)
    if delete:
        await message.delete()
    keyboard = await create_message_keyboard(data=data)
    has_youtube = await has_text_youtube_link(text)
    if video:
        if has_youtube:
            await message.answer_video(video=video)
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer_video(video=video, caption=text, reply_markup=keyboard)
    elif gif:
        if has_youtube:
            await message.answer_animation(animation=gif)
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer_animation(animation=gif, caption=text, reply_markup=keyboard)
    elif audio:
        if has_youtube:
            await message.answer_audio(audio=audio)
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer_audio(audio=audio, caption=text, reply_markup=keyboard)
    elif document:
        if has_youtube:
            await message.answer_document(document=document)
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer_document(document=document, caption=text, reply_markup=keyboard)
    elif photo:
        if has_youtube:
            await message.answer_photo(photo=photo)
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
    elif video_note:
        await message.answer_video_note(video_note=video_note)
        await message.answer(text, reply_markup=keyboard)
    elif voice:
        await message.answer_voice(voice=voice)
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer(text=text, reply_markup=keyboard)
