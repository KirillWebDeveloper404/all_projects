from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

edit_message_kb_data = CallbackData('edit_message_kb_data', 'prefix')


async def generate_edit_messages_keyboard(data):
    inline_keyboard = []

    row_1 = []  # Фото // Гифка // Видео

    photo = data['photo']
    gif = data['gif']
    video = data['video']

    if photo:
        row_1.append(InlineKeyboardButton('✔ ️Фото', callback_data=edit_message_kb_data.new(prefix='photo')))
    else:
        row_1.append(InlineKeyboardButton('Фото', callback_data=edit_message_kb_data.new(prefix='photo')))

    if gif:
        row_1.append(InlineKeyboardButton('✔ ️Гифка', callback_data=edit_message_kb_data.new(prefix='gif')))
    else:
        row_1.append(InlineKeyboardButton('Гифка', callback_data=edit_message_kb_data.new(prefix='gif')))

    if video:
        row_1.append(InlineKeyboardButton('✔ ️Видео', callback_data=edit_message_kb_data.new(prefix='video')))
    else:
        row_1.append(InlineKeyboardButton('Видео', callback_data=edit_message_kb_data.new(prefix='video')))

    row_2 = []  # Аудио // Войс // Т видео

    audio = data['audio']
    voice = data['voice']
    video_note = data['video_note']
    if audio:
        row_2.append(InlineKeyboardButton('✔ Аудио', callback_data=edit_message_kb_data.new(prefix='audio')))
    else:
        row_2.append(InlineKeyboardButton('Аудио', callback_data=edit_message_kb_data.new(prefix='audio')))

    if voice:
        row_2.append(InlineKeyboardButton('✔ Войс', callback_data=edit_message_kb_data.new(prefix='voice')))
    else:
        row_2.append(InlineKeyboardButton('Войс', callback_data=edit_message_kb_data.new(prefix='voice')))

    if video_note:
        row_2.append(InlineKeyboardButton('✔ Т Видео', callback_data=edit_message_kb_data.new(prefix='video_note')))
    else:
        row_2.append(InlineKeyboardButton('Т Видео', callback_data=edit_message_kb_data.new(prefix='video_note')))

    row_3 = []  # Текст // Квиз // Файл

    text = data['text']
    test = data['test']
    document = data['document']

    if text:
        row_3.append(InlineKeyboardButton('✔ Текст', callback_data=edit_message_kb_data.new(prefix='text')))
    else:
        row_3.append(InlineKeyboardButton('Текст', callback_data=edit_message_kb_data.new(prefix='text')))

    if test:
        row_3.append(InlineKeyboardButton('✔ Квиз', callback_data=edit_message_kb_data.new(prefix='test')))
    else:
        row_3.append(InlineKeyboardButton('Квиз', callback_data=edit_message_kb_data.new(prefix='test')))

    if document:
        row_3.append(InlineKeyboardButton('✔ Файл', callback_data=edit_message_kb_data.new(prefix='document')))
    else:
        row_3.append(InlineKeyboardButton('Файл', callback_data=edit_message_kb_data.new(prefix='document')))

    row_4 = []  # Отправка // Задержка // Удаление
    if data['type_message'] != 'test':
        # if not data['send_day'] or not data['send_hour'] or not data['send_minute']:
        #     if data['interval_hour'] and not data['interval_minute'] and not data['interval_day'] \
        #             and not data['interval_second']:
        #         row_4.append(InlineKeyboardButton('Отправка', callback_data=edit_message_kb_data.new(prefix='send')))
        # else:
        #     row_4.append(InlineKeyboardButton('✔ Отправка', callback_data=edit_message_kb_data.new(prefix='send')))
        #
        # if not data['interval_hour'] and not data['interval_minute'] and not data['interval_day'] \
        #         and not data['interval_second']:
        #     if not data['send_day'] or not data['send_hour'] or not data['send_minute']:
        #         row_4.append(
        #             InlineKeyboardButton('Задержка', callback_data=edit_message_kb_data.new(prefix='interval')))
        # else:
        #     row_4.append(InlineKeyboardButton('✔ Задержка', callback_data=edit_message_kb_data.new(prefix='interval')))

        if not data['delete_hour'] and not data['delete_second'] and not data['delete_minute'] \
                and not data['delete_day']:
            row_4.append(InlineKeyboardButton('Удаление', callback_data=edit_message_kb_data.new(prefix='delete')))
        else:
            row_4.append(InlineKeyboardButton('✔ Удаление', callback_data=edit_message_kb_data.new(prefix='delete')))

    if not data['link']:
        row_4.append(InlineKeyboardButton('Кнопка', callback_data=edit_message_kb_data.new(prefix='button_link')))
    else:
        row_4.append(InlineKeyboardButton('✔ Кнопка', callback_data=edit_message_kb_data.new(prefix='button_link')))

    row_5 = []
    row_5.append(InlineKeyboardButton('Сохранить', callback_data=edit_message_kb_data.new('save')))

    inline_keyboard.append(row_1)
    inline_keyboard.append(row_2)
    inline_keyboard.append(row_3)
    inline_keyboard.append(row_4)
    inline_keyboard.append(row_5)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
