from loader import bot
from modules.DataBase import get_message_af_by_id, get_question_by_id


async def send_manage_message_funnel(message_id, chat_id, keyboard):
    message = get_message_af_by_id(message_id)
    type_message = message.type_message
    text = ''
    if type_message == 'content':
        type_message = 'Тип сообщения:контент\n'
    else:
        type_message = 'Тип сообщения:оповещение\n'
    text += f'{type_message}\n'
    if message.day:
        text += f'Отправка: {message.day} день в {message.hour}:{message.minute}\n\n'

    # Проверка задержки
    if message.interval_msg_id:
        int_message = get_message_af_by_id(message.interval_msg_id)

        if not message.interval_day:
            interval_day = 0
        else:
            interval_day = message.interval_day
        if not message.interval_hour:
            interval_hour = 0
        else:
            interval_hour = message.interval_hour
        if not message.interval_minute:
            interval_minute = 0
        else:
            interval_minute = message.interval_minute
        if not message.interval_second:
            interval_second = 0
        else:
            interval_second = message.interval_second

        text += f'Отправка: задержка в {interval_day} дней {interval_hour} часов {interval_minute} минут ' \
                f'{interval_second} секунд от {int_message.day} дня {int_message.hour}: {int_message.minute}\n\n'

    if message.delete_hour or message.delete_minute or message.delete_day or message.delete_second:
        text += f'Удаление: через {message.delete_day} дней {message.delete_hour} часов {message.delete_minute} ' \
                f'минут {message.delete_second} секунд от отправки сообщения\n\n'

    else:
        text += 'Удаление: отсутствует\n\n'

    if message.link:
        text += 'Кнопка: есть\n' \
                f'Ссылка: {message.link}\n' \
                f'Текст ссылки: {message.text_link}\n\n'
    else:
        text += 'Кнопка: отсутствует\n\n'

    if message.test:
        question = get_question_by_id(message.test)
        if question:
            text += f'Вопрос: {question.text}\n'
        else:
            text += 'Вопрос: был прикреплен, но вы удалили этот вопрос\n'
    else:
        text += 'Вопрос: отсутствует\n'

    text += '===================\n'

    msg_text = message.message_text
    if msg_text:
        text += f'Сообщение:\n{msg_text}'

    if message.photo:
        await bot.send_photo(chat_id=chat_id, caption=text, photo=message.photo, reply_markup=keyboard)
    elif message.gif:
        await bot.send_animation(chat_id=chat_id, caption=text, animation=message.gif, reply_markup=keyboard)
    elif message.video:
        await bot.send_video(chat_id=chat_id, caption=text, video=message.video, reply_markup=keyboard)
    elif message.voice:
        await bot.send_voice(chat_id=chat_id, caption=text, voice=message.voice, reply_markup=keyboard)
    elif message.video_note:
        await bot.send_video_note(chat_id=chat_id, video_note=message.video_note)
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
    elif message.document:
        await bot.send_document(chat_id=chat_id, document=message.document, caption=text, reply_markup=keyboard)
    elif message.audio:
        await bot.send_audio(chat_id=chat_id, audio=message.audio, caption=text, reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)