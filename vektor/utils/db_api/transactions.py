import datetime

import peewee

from utils.db_api.base import BaseModel


class Transaction(BaseModel):
    user_id = peewee.BigIntegerField()
    amount = peewee.IntegerField()
    ts = peewee.DateTimeField(default=datetime.datetime.now())

    class Meta:
        table_name = 'transaction'


async def save_transaction(user_id: int, amount: int):
    transaction = Transaction(user_id=user_id, amount=amount)
    transaction.save()
    return transaction


async def select_transactions_by_user_id(user_id: int):
    transactions = Transaction.select().where(Transaction.user_id == user_id).execute()
    return [transaction.amount for transaction in transactions]
