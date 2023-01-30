from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboard.inline.create_message_af.all_data import create_message_funnel, close_add_message_funnel

create_message_af = CallbackData('create_message_af', 'prefix')


async def create_message_keyboard(data):
    inline_keyboard = []
    row_1 = []  # Фото // Гифка // Видео

    if data['photo'] or data['gif'] or data['video'] or data['audio'] or data['voice'] or data['video_note'] \
            or data['document']:
        media = True
    else:
        media = False

    if not data['photo']:
        if not media:
            row_1.append(InlineKeyboardButton('Фото', callback_data=create_message_af.new(prefix='photo')))
    else:
        row_1.append(InlineKeyboardButton('✔ ️Фото', callback_data=create_message_af.new(prefix='photo')))

    if not data['gif']:
        if not media:
            row_1.append(InlineKeyboardButton('Гифка', callback_data=create_message_af.new(prefix='gif')))
    else:
        row_1.append(InlineKeyboardButton('✔ ️Гифка', callback_data=create_message_af.new(prefix='gif')))

    if not data['video']:
        if not media:
            row_1.append(InlineKeyboardButton('Видео', callback_data=create_message_af.new(prefix='video')))
    else:
        row_1.append(InlineKeyboardButton('✔ Видео', callback_data=create_message_af.new(prefix='video')))

    row_2 = []  # Аудио // Войс // Т видео

    if not data['audio']:
        if not media:
            row_2.append(InlineKeyboardButton('Аудио', callback_data=create_message_af.new(prefix='audio')))
    else:
        row_2.append(InlineKeyboardButton('✔ Аудио', callback_data=create_message_af.new(prefix='audio')))

    if not data['voice']:
        if not media and not data['text']:
            row_2.append(InlineKeyboardButton('Войс', callback_data=create_message_af.new(prefix='voice')))
    else:
        row_2.append(InlineKeyboardButton('✔ Войс', callback_data=create_message_af.new(prefix='voice')))

    if not data['video_note']:
        if not media and not data['text']:
            row_2.append(InlineKeyboardButton('Т видео', callback_data=create_message_af.new(prefix='video_note')))
    else:
        row_2.append(InlineKeyboardButton('✔ Т видео', callback_data=create_message_af.new(prefix='video_note')))

    row_3 = []  # Текст // Квиз // Файл

    if not data['text']:
        if not data['voice'] and not data['video_note']:
            row_3.append(InlineKeyboardButton('Текст', callback_data=create_message_af.new(prefix='text')))

    else:
        row_3.append(InlineKeyboardButton('✔ Текст', callback_data=create_message_af.new(prefix='text')))

    if not data['test']:
        row_3.append(InlineKeyboardButton('Квиз', callback_data=create_message_af.new(prefix='test')))
    else:
        row_3.append(InlineKeyboardButton('✔ Квиз', callback_data=create_message_af.new(prefix='test')))

    if not data['document']:
        if not media:
            row_3.append(InlineKeyboardButton('Файл', callback_data=create_message_af.new(prefix='document')))
    else:
        row_3.append(InlineKeyboardButton('✔ Файл', callback_data=create_message_af.new(prefix='document')))

    row_4 = []  # Отправка // Задержка // Удаление

    if not data['hour'] and not data['minute'] and not data['day']:
        if not data['interval_hour'] and not data['interval_minute'] and data['type'] != 'first':
            row_4.append(InlineKeyboardButton('Отправка', callback_data=create_message_af.new(prefix='send')))
    else:
        row_4.append(InlineKeyboardButton('✔ Отправка', callback_data=create_message_af.new(prefix='send')))

    if not data['interval_hour'] and not data['interval_minute'] and not data['interval_day'] and not data[
        'interval_second']:
        if not data['hour'] and not data['day'] and not data['minute'] and data['type'] != 'first' \
                and data['type'] != 'system':
            row_4.append(InlineKeyboardButton('Задержка', callback_data=create_message_af.new(prefix='interval')))
    else:
        row_4.append(InlineKeyboardButton('✔ Задержка', callback_data=create_message_af.new(prefix='interval')))

    if not data['delete_hour'] and not data['delete_second'] and not data['delete_minute'] and not data['delete_day']:
        row_4.append(InlineKeyboardButton('Удаление', callback_data=create_message_af.new(prefix='delete_hour')))
    else:
        row_4.append(InlineKeyboardButton('✔ Удаление', callback_data=create_message_af.new(prefix='delete_hour')))

    row_5 = []

    if not data['link']:
        row_5.append(InlineKeyboardButton('Кнопка', callback_data=create_message_af.new(prefix='button_link')))
    else:
        row_5.append(InlineKeyboardButton('✔ Кнопка', callback_data=create_message_af.new(prefix='button_link')))

    row_6 = []

    if data['link'] or data['delete_hour'] or data['interval_hour'] or data['hour'] or data['minute'] or data[
        'document'] or data['test'] or data['text'] or data['video_note'] or data['voice'] or data['audio'] \
            or data['video'] or data['gif'] or data['photo']:
        row_6.append(InlineKeyboardButton('Очистить', callback_data=create_message_af.new(prefix='clear')))
    if (data['test'] or (data['text'] or data['video_note'] or data['voice'] or data['photo'] or data['audio'] or data['gif'] or data[
        'document'] or data['video'])) and (
            (data['day'] and (data['minute'] or data['minute'] == 0) and (data['hour'] or data['hour'] == 0)) or
            (data['interval_hour'] or data['interval_minute'] or data['interval_day'] or data['interval_second'])):
        row_6.append(InlineKeyboardButton('+ Сообщение', callback_data=create_message_funnel.new(
            msg_type=data['type'], funnel_id=data['funnel_id'], save='Yes'
        )))

    row_7 = []
    if (data['type'] == 'first' and not data['is_fast_start']) and ((
            data['text'] or data['video_note'] or data['voice'] or data['photo'] or data['audio'] or data['gif'] or
            data['document'] or data['video']) or data['test']):
        row_7.append(
            InlineKeyboardButton('Перейти к системным сообщениям', callback_data=create_message_funnel.new(
                msg_type='system', funnel_id=data['funnel_id'], save='Yes'
            )))

    if (data['type'] == 'system' and ((data['test'] or
            data['text'] or data['video_note'] or data['voice'] or data['photo'] or data['audio'] or data['gif'] or
            data['document'] or data['video'])) and (
                data['day'] and (data['minute'] or data['minute'] == 0) and (data['hour'] or data['hour'] == 0))) or \
            ((data['is_fast_start'] and (data['test'] or (
                    data['text'] or data['video_note'] or data['voice'] or data['photo'] or data['audio'] or
                    data['gif'] or data['document'] or data['video']))) and data['type'] != 'content'):
        row_7.append(InlineKeyboardButton('Перейти к наполнению воронки', callback_data=create_message_funnel.new(
            msg_type='content', funnel_id=data['funnel_id'], save='Yes'
        )))

    if (data['type'] == 'content' or data['is_add_exit']) and (
            (data['test'] or (data['text'] or data['video_note'] or data['voice'] or data['photo'] or data['audio'] or data['gif']
             or data['document'] or data['video'])) and \
            ((data['day'] and (data['minute'] or data['minute'] == 0) and (data['hour'] or data['hour'] == 0)) or
             (data['interval_hour'] or data['interval_minute'] or data['interval_day'] or data['interval_second']))):
        row_7.append(InlineKeyboardButton('Закончить наполнение воронки', callback_data=close_add_message_funnel.new(
            prefix='close'
        )))
    inline_keyboard.append(row_1)
    inline_keyboard.append(row_2)
    inline_keyboard.append(row_3)
    inline_keyboard.append(row_4)
    inline_keyboard.append(row_5)
    inline_keyboard.append(row_6)
    inline_keyboard.append(row_7)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
