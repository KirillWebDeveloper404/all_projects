import logging

from modules.DataBase import get_all_users, get_users_passed_entrance_test, get_users_not_moms, get_users_pregnant, \
    get_users_moms, get_users_first_stage, get_users_second_stage, get_users_third_stage, get_users_bought_product, \
    get_users_not_bought_product, get_users_april_start, get_users_af_by_funnel_id, get_auto_funnels_segment


async def get_users(data):
    if data == "all":
        segment = get_all_users()
    elif data == "entrance_test":
        segment = get_users_passed_entrance_test()
    elif data == "not_moms":
        segment = get_users_not_moms()
    elif data == "pregnant":
        segment = get_users_pregnant()
    elif data == "moms":
        segment = get_users_moms()
    elif data == "first_stage":
        segment = get_users_first_stage()
    elif data == "second_stage":
        segment = get_users_second_stage()
    elif data == "third_stage":
        segment = get_users_third_stage()
    elif data.startswith("bought_product_"):
        product_id = int(data.split("bought_product_")[1])
        segment = get_users_bought_product(product_id)
    elif data.startswith("not_bought_product_"):
        product_id = int(data.split("not_bought_product_")[1])
        segment = get_users_not_bought_product(product_id)
    elif data == 'april_start':
        segment = get_users_april_start()
    elif data.startswith('funnel_'):
        funnel_id = int(data.split('funnel_')[1])
        segment = get_auto_funnels_segment(funnel_id)
    else:
        logging.error(f"Mailing category {data} is not known, sending to all users")
        segment = get_all_users()

    return segment