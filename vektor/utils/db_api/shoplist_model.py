import datetime

import peewee

from utils.db_api.base import BaseModel
from utils.db_api.rates_model import Rates
from utils.db_api.users_model import Users, get_user_by_chat_id


class ShopList(BaseModel):
    price = peewee.IntegerField()
    user = peewee.ForeignKeyField(Users, on_delete='CASCADE')
    rate = peewee.ForeignKeyField(Rates, on_delete='CASCADE')
    ts = peewee.DateTimeField(default=datetime.datetime.now())

    class Meta:
        table_name = 'shop_list'


async def create_order(price, rate, chat_id):
    user = await get_user_by_chat_id(chat_id=chat_id)
    order = ShopList(price=price, rate=rate, user=user.id)
    order.save()
    return order
