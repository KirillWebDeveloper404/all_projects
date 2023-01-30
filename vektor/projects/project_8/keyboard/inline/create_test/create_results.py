from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

create_message_result = CallbackData('create_message_result', 'prefix')


async def create_result_msg_keyboard(data):
    inline_keyboard = []
    row_1 = []  # Фото // Гифка // Видео
    row_2 = []  # Аудио // Войс // Т видео
    row_3 = []  # Текст // Квиз // Файл
    row_4 = []  # Кнопка // очистить
    row_5 = []  # Сохранить/пропустить

    photo = data['photo']
    text = data['result_text']
    gif = data['gif']
    video = data['video']
    audio = data['audio']
    voice = data['voice']
    video_note = data['video_note']
    test = data['test']
    document = data['document']
    link = data['link']

    if photo or gif or video or audio or voice or video_note or document:
        media = True
    else:
        media = False

    if not photo:
        if not media:
            row_1.append(InlineKeyboardButton('Фото', callback_data=create_message_result.new(prefix='photo')))
    else:
        row_1.append(InlineKeyboardButton('✔ ️Фото', callback_data=create_message_result.new(prefix='photo')))

    if not gif:
        if not media:
            row_1.append(InlineKeyboardButton('Гифка', callback_data=create_message_result.new(prefix='gif')))
    else:
        row_1.append(InlineKeyboardButton('✔ ️Гифка', callback_data=create_message_result.new(prefix='gif')))

    if not video:
        if not media:
            row_1.append(InlineKeyboardButton('Видео', callback_data=create_message_result.new(prefix='video')))
    else:
        row_1.append(InlineKeyboardButton('✔ Видео', callback_data=create_message_result.new(prefix='video')))

    if not audio:
        if not media:
            row_2.append(InlineKeyboardButton('Аудио', callback_data=create_message_result.new(prefix='audio')))
    else:
        row_2.append(InlineKeyboardButton('✔ Аудио', callback_data=create_message_result.new(prefix='audio')))

    if not voice:
        if not media and not text:
            row_2.append(InlineKeyboardButton('Войс', callback_data=create_message_result.new(prefix='voice')))
    else:
        row_2.append(InlineKeyboardButton('✔ Войс', callback_data=create_message_result.new(prefix='voice')))

    if not video_note:
        if not media and not text:
            row_2.append(InlineKeyboardButton('Т видео', callback_data=create_message_result.new(prefix='video_note')))
    else:
        row_2.append(InlineKeyboardButton('✔ Т видео', callback_data=create_message_result.new(prefix='video_note')))

    if not text:
        if not voice and not video_note:
            row_3.append(InlineKeyboardButton('Текст', callback_data=create_message_result.new(prefix='text')))

    else:
        row_3.append(InlineKeyboardButton('✔ Текст', callback_data=create_message_result.new(prefix='text')))

    if not test:
        row_3.append(InlineKeyboardButton('Квиз', callback_data=create_message_result.new(prefix='test')))
    else:
        row_3.append(InlineKeyboardButton('✔ Квиз', callback_data=create_message_result.new(prefix='test')))

    if not document:
        if not media:
            row_3.append(InlineKeyboardButton('Файл', callback_data=create_message_result.new(prefix='document')))
    else:
        row_3.append(InlineKeyboardButton('✔ Файл', callback_data=create_message_result.new(prefix='document')))

    if not link:
        if media or text:
            row_4.append(InlineKeyboardButton('Кнопка', callback_data=create_message_result.new(prefix='button')))
    else:
        row_4.append(InlineKeyboardButton('✔ Кнопка', callback_data=create_message_result.new(prefix='button')))

    if media or link or text or test:
        row_4.append(InlineKeyboardButton('Очистить', callback_data=create_message_result.new(prefix='clear')))

    row_5.append(
        InlineKeyboardButton('Сохранить/пропустить', callback_data=create_message_result.new(prefix='save')))

    inline_keyboard.append(row_1)
    inline_keyboard.append(row_2)
    inline_keyboard.append(row_3)
    inline_keyboard.append(row_4)
    inline_keyboard.append(row_5)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
