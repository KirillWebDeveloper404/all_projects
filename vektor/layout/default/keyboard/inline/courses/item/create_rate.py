from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

create_rate_course_data = CallbackData('create_rt_cr', 'pr')


async def get_create_rate_course_kb(data):
    inline_keyboard = []

    row_1 = []  # Название // Описание // Медиа
    row_2 = []  # Цена // Рассрочка // Куратор
    row_3 = []  # Старт // Длительность // Закрытие
    row_4 = []  # Демо // Чат // Канал
    row_5 = []  # Отменить // Бонус
    row_6 = []  # Сохранить

    if data['name']:
        row_1.append(InlineKeyboardButton('✔️ Название', callback_data=create_rate_course_data.new(
            pr='name'
        )))
    else:
        row_1.append(InlineKeyboardButton('Название', callback_data=create_rate_course_data.new(
            pr='name'
        )))

    if data['desc']:
        row_1.append(InlineKeyboardButton('✔️ Описание', callback_data=create_rate_course_data.new(
            pr='desc'
        )))
    else:
        row_1.append(InlineKeyboardButton('Описание', callback_data=create_rate_course_data.new(
            pr='desc'
        )))

    if data['media']:
        row_1.append(InlineKeyboardButton('✔️ Медиа', callback_data=create_rate_course_data.new(
            pr='media'
        )))
    else:
        row_1.append(InlineKeyboardButton('Медиа', callback_data=create_rate_course_data.new(
            pr='media'
        )))

    if data['price']:
        row_2.append(InlineKeyboardButton('✔️ Цена', callback_data=create_rate_course_data.new(
            pr='price'
        )))
    else:
        row_2.append(InlineKeyboardButton('Цена', callback_data=create_rate_course_data.new(
            pr='price'
        )))

    if data['intallment']:
        row_2.append(InlineKeyboardButton('✔️ Рассрочка', callback_data=create_rate_course_data.new(
            pr='intallment_pay'
        )))
    else:
        row_2.append(InlineKeyboardButton('Рассрочка', callback_data=create_rate_course_data.new(
            pr='intallment_pay'
        )))

    if data['curator']:
        row_2.append(InlineKeyboardButton('✔️ Куратор', callback_data=create_rate_course_data.new(
            pr='curator'
        )))
    else:
        row_2.append(InlineKeyboardButton('Куратор', callback_data=create_rate_course_data.new(
            pr='curator'
        )))

    if data['type_start']:
        row_3.append(InlineKeyboardButton('✔️ Старт', callback_data=create_rate_course_data.new(
            pr='start'
        )))
    else:
        row_3.append(InlineKeyboardButton('Старт', callback_data=create_rate_course_data.new(
            pr='start'
        )))

    if data['duration']:
        row_3.append(InlineKeyboardButton('✔️ Длительность', callback_data=create_rate_course_data.new(
            pr='duration'
        )))
    else:
        row_3.append(InlineKeyboardButton('Длительность', callback_data=create_rate_course_data.new(
            pr='duration'
        )))

    if data['close_time']:
        row_3.append(InlineKeyboardButton('✔️ Закрытие', callback_data=create_rate_course_data.new(
            pr='close_time'
        )))
    else:
        row_3.append(InlineKeyboardButton('Закрытие', callback_data=create_rate_course_data.new(
            pr='close_time'
        )))

    if data['demo']:
        row_4.append(InlineKeyboardButton('✔️ Демо', callback_data=create_rate_course_data.new(
            pr='demo'
        )))
    else:
        row_4.append(InlineKeyboardButton('Демо', callback_data=create_rate_course_data.new(
            pr='demo'
        )))

    if data['chat']:
        row_4.append(InlineKeyboardButton('✔️ Чат', callback_data=create_rate_course_data.new(
            pr='chat'
        )))
    else:
        row_4.append(InlineKeyboardButton('Чат', callback_data=create_rate_course_data.new(
            pr='chat'
        )))

    if data['channel']:
        row_4.append(InlineKeyboardButton('✔️ Канал', callback_data=create_rate_course_data.new(
            pr='channel'
        )))
    else:
        row_4.append(InlineKeyboardButton('Канал', callback_data=create_rate_course_data.new(
            pr='channel'
        )))

    row_5.append(InlineKeyboardButton('Отменить', callback_data=create_rate_course_data.new(
        pr='cancel'
    )))
    if data['bonus']:
        row_5.append(InlineKeyboardButton('✔️ Канал', callback_data=create_rate_course_data.new(
            pr='bonus'
        )))
    else:
        row_5.append(InlineKeyboardButton('Бонус', callback_data=create_rate_course_data.new(
            pr='bonus'
        )))

    if data['start'] and data['name'] and data['desc'] and data['price'] and data['duration'] and data['close_time']:
        row_6.append(InlineKeyboardButton('Сохранить и опубликовать', callback_data=create_rate_course_data.new(
            pr='save'
        )))

    inline_keyboard.append(row_1)
    inline_keyboard.append(row_2)
    inline_keyboard.append(row_3)
    inline_keyboard.append(row_4)
    inline_keyboard.append(row_5)
    inline_keyboard.append(row_6)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
