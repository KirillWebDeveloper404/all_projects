from aiogram import types

from keyboard.inline.edit.edit_message import generate_edit_messages_keyboard
from loader import bot


async def get_text_edit_messages(data: dict, message: types.Message, keyboard=None, delete=False):
    if not keyboard:
        keyboard = await generate_edit_messages_keyboard(data)

    if delete:
        await message.delete()
    text = ''
    if data['type_message'] == 'system':
        text += 'Тип сообщение: Напоминание\n'
    elif data['type_message'] == 'content':
        text += 'Тип сообщение: Контент\n'
    else:
        text += 'Тип сообщения: Квиз\n'

    if data['delete_second'] or data['delete_minute'] or data['delete_hour'] or data['delete_day']:
        text += f'Удаление: через {data["delete_second"]} сек {data["delete_minute"]} мин {data["delete_hour"]} ' \
                f'часов {data["delete_day"]} дней \n\n'

    if data['link']:
        text += f'Ссылка: {data["link"]}\nТекст кнопки: {data["text_link"]}\n\n'

    if data['send_day'] or data['send_hour'] or data['send_minute']:
        text += f'Отправка: на {data["send_day"]} день в {data["send_hour"]}:{data["send_minute"]}\n\n'

    if data['interval_msg']:
        # TODO: Добавить интервальное сообщение
        text += f'Задержка: {data["interval_second"]} секунд {data["interval_minute"]} минут' \
                f' {data["interval_hour"]} часов {data["interval_day"]} дней\n\n'

    if data['test']:
        # TODO: Добавить тестирование
        pass

    text += '=======================\n'
    text += f'Сообщение:\n{data["text"]}'

    if data['photo']:
        await message.answer_photo(photo=data['photo'], caption=text, reply_markup=keyboard)
    elif data['gif']:
        await message.answer_animation(animation=data['gif'], caption=text, reply_markup=keyboard)
    elif data['document']:
        await message.answer_document(document=data['document'], caption=text, reply_markup=keyboard)
    elif data['video']:
        await message.answer_video(video=data['video'], caption=text, reply_markup=keyboard)
    elif data['video_note']:
        await message.answer_video_note(video_note=data['video_note'])
        await message.answer(text=text, reply_markup=keyboard)
    elif data['voice']:
        await message.answer_voice(voice=data['voice'], caption=text, reply_markup=keyboard)
    elif data['audio']:
        await message.answer_audio(audio=data['audio'], caption=text, reply_markup=keyboard)
    else:
        await message.answer(text=text, reply_markup=keyboard)
