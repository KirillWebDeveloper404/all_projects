from utils.db_api.rates_model import create_rate, get_rate_by_id


async def add_rates_test():
    RATE_DEFAULT = 1
    rate = await get_rate_by_id(RATE_DEFAULT)
    if rate:
        pass
    else:
        await create_rate(name="Тестовый тариф", price=0, desc="Пробный тариф", path="layout/default")
