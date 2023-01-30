from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

edit_message_af_and_tests = CallbackData('edit_super_message', 'prefix')


async def get_edit_keyboard(data):
    inline_keyboard = []

    type_message = data['type_message']  # test, system, content

    photo = data['photo']
    gif = data['gif']
    document = data['document']
    video = data['video']
    video_note = data['document']
    voice = data['document']
    audio = data['audio']
    message_text = data['text']
    link = data['link']
    delete_second = data['delete_second']
    delete_minute = data['delete_minute']
    delete_hour = data['delete_hour']
    delete_day = data['delete_day']
    send_day = data['send_day']
    send_hour = data['send_hour']
    send_minute = data['send_minute']
    is_first = data['is_first']
    interval_second = data['interval_second']
    interval_minute = data['interval_minute']
    interval_hour = data['interval_hour']
    interval_day = data['interval_day']
    test = data['test']

    if photo or gif or video or audio or voice or video_note or document:
        media = True
    else:
        media = False

    row_1 = []
    row_2 = []
    row_3 = []  # Текст // Квиз // Файл
    row_4 = []  # Отправка // Задержка // Удаление (Эта строчка есть только в автоворонках)
    row_5 = []
    row_6 = []

    if not photo:
        if not media:
            row_1.append(InlineKeyboardButton('Фото', callback_data=edit_message_af_and_tests.new(prefix='photo')))
    else:
        row_1.append(InlineKeyboardButton('✔ ️Фото', callback_data=edit_message_af_and_tests.new(prefix='photo')))

    if not gif:
        if not media:
            row_1.append(InlineKeyboardButton('Гифка', callback_data=edit_message_af_and_tests.new(prefix='gif')))
    else:
        row_1.append(InlineKeyboardButton('✔ ️Гифка', callback_data=edit_message_af_and_tests.new(prefix='gif')))

    if not video:
        if not media:
            row_1.append(InlineKeyboardButton('Видео', callback_data=edit_message_af_and_tests.new(prefix='video')))
    else:
        row_1.append(InlineKeyboardButton('✔ Видео', callback_data=edit_message_af_and_tests.new(prefix='video')))

    if not audio:
        if not media:
            row_2.append(InlineKeyboardButton('Аудио', callback_data=edit_message_af_and_tests.new(prefix='audio')))
    else:
        row_2.append(InlineKeyboardButton('✔ Аудио', callback_data=edit_message_af_and_tests.new(prefix='audio')))

    if not voice:
        if not media and not message_text:
            row_2.append(InlineKeyboardButton('Войс', callback_data=edit_message_af_and_tests.new(prefix='voice')))
    else:
        row_2.append(InlineKeyboardButton('✔ Войс', callback_data=edit_message_af_and_tests.new(prefix='voice')))

    if not video_note:
        if not media and not message_text:
            row_2.append(
                InlineKeyboardButton('Т видео', callback_data=edit_message_af_and_tests.new(prefix='video_note')))
    else:
        row_2.append(
            InlineKeyboardButton('✔ Т видео', callback_data=edit_message_af_and_tests.new(prefix='video_note')))

    if not message_text:
        if not voice and not video_note:
            row_3.append(InlineKeyboardButton('Текст', callback_data=edit_message_af_and_tests.new(prefix='text')))

    else:
        row_3.append(InlineKeyboardButton('✔ Текст', callback_data=edit_message_af_and_tests.new(prefix='text')))

    if not test:
        row_3.append(InlineKeyboardButton('Квиз', callback_data=edit_message_af_and_tests.new(prefix='test')))
    else:
        row_3.append(InlineKeyboardButton('✔ Квиз', callback_data=edit_message_af_and_tests.new(prefix='test')))

    if not document:
        if not media:
            row_3.append(InlineKeyboardButton('Файл', callback_data=edit_message_af_and_tests.new(prefix='document')))
    else:
        row_3.append(InlineKeyboardButton('✔ Файл', callback_data=edit_message_af_and_tests.new(prefix='document')))

    if type_message != 'test':
        if not send_hour and not send_minute and not send_day:
            if not interval_hour and not interval_minute and not is_first and not interval_second and not interval_day:
                row_4.append(
                    InlineKeyboardButton('Отправка', callback_data=edit_message_af_and_tests.new(prefix='send')))
        else:
            row_4.append(InlineKeyboardButton('✔ Отправка', callback_data=edit_message_af_and_tests.new(prefix='send')))

        if not interval_hour and not interval_minute and not is_first and not interval_second and not interval_day:
            if not send_hour and not send_day and not send_minute and not is_first and type_message != 'system':
                row_4.append(
                    InlineKeyboardButton('Задержка', callback_data=edit_message_af_and_tests.new(prefix='interval')))
        else:
            row_4.append(
                InlineKeyboardButton('✔ Задержка', callback_data=edit_message_af_and_tests.new(prefix='interval')))

        if not delete_hour and not delete_second and not delete_minute and not delete_day:
            row_4.append(InlineKeyboardButton('Удаление', callback_data=edit_message_af_and_tests.new(prefix='del')))
        else:
            row_4.append(InlineKeyboardButton('✔ Удаление', callback_data=edit_message_af_and_tests.new(prefix='del')))

    if not link:
        row_5.append(InlineKeyboardButton('Кнопка', callback_data=edit_message_af_and_tests.new(prefix='button')))
    else:
        row_5.append(InlineKeyboardButton('✔ Кнопка', callback_data=edit_message_af_and_tests.new(prefix='button')))

    row_6.append(
        InlineKeyboardButton('Сохранить и выйти', callback_data=edit_message_af_and_tests.new(prefix='save_close')))
    inline_keyboard.append(row_1)
    inline_keyboard.append(row_2)
    inline_keyboard.append(row_3)
    inline_keyboard.append(row_4)
    inline_keyboard.append(row_5)
    inline_keyboard.append(row_6)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
