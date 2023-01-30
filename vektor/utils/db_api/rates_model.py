import peewee

from utils.db_api.base import BaseModel


class Rates(BaseModel):
    name = peewee.TextField()
    desc = peewee.TextField()
    path = peewee.TextField()
    price = peewee.IntegerField()


async def create_rate(name, price, desc, path):
    rate = Rates(name=name, price=price, desc=desc, path=path)
    rate.save()
    return rate


async def change_rate_info(rate_id, name=None, price=None, desc=None):
    rate = Rates.select().where(Rates.id == rate_id).get()
    if name:
        rate.name = name
    if price:
        rate.price = price
    if desc:
        rate.desc = desc
    rate.save()
    return rate


async def get_rate_by_id(rate_id):
    try:
        return Rates.select().where(Rates.id == rate_id).get()
    except:
        return None


async def get_all_rates():
    return Rates.select()


async def del_rate_by_id(rate_id):
    rate = Rates.get(Rates.id == rate_id)
    rate.delete_instance()
