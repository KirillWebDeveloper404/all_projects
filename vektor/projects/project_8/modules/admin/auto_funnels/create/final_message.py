from modules.DataBase import get_name_product, get_auto_funnel_by_id
from utils.functions import translate_week_day


async def get_final_message(data):
    name = data['name']
    text = f'Автоворонка\n'
    if name:
           text += f'Название: {name}\n'
    is_start_on_week = data['is_start_on_week']
    is_start_on_day_month = data['is_start_on_day_month']
    fast_start = data['fast_start']

    product = data['product']
    buy_job = data['if_buy']
    not_buy_job = data['if_not_buy']


    if is_start_on_week:
        start_on_week = data['start_on_week']
        start_on_week = await translate_week_day(start_on_week)
        text += f'Начало в {start_on_week}\n'
    elif is_start_on_day_month:
        start_on_day_month = data['start_on_day_month']
        text += f'Начало в {start_on_day_month} день месяца\n'
    elif fast_start:
        text += f'Начало: Мгновенно\n'

    if product:
        product_name = get_name_product(product)
        text += f'Продукт: {product_name}\n'


    if buy_job:
        if buy_job == 'stop':
            text += 'После покупки: будет остоновлен\n'
        else:
            funnel = get_auto_funnel_by_id(int(buy_job))
            text += f'После покупки: редирект на воронку {funnel.name}\n'

    if not_buy_job:
        funnel = get_auto_funnel_by_id(int(not_buy_job))
        text += f'Если не купил: редирект на воронку {funnel.name}\n'

    return text
