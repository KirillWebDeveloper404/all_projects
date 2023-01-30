import peewee

from .base import BaseTSModel


class Users(BaseTSModel):
    chat_id = peewee.IntegerField(unique=True)
    username = peewee.TextField(null=True)
    phone = peewee.TextField(null=True)
    referral = peewee.IntegerField(null=True)
    free_days = peewee.IntegerField(default=14)
    free_active = peewee.BooleanField(default=False)
    balance = peewee.IntegerField(default=0)
    trial_activate = peewee.BooleanField(default=False)
    is_payment = peewee.BooleanField(default=False)
    utc_timezone = peewee.TextField(null=True)

    class Meta:
        table_name = 'users'


async def update_utc_timezone(chat_id, utc_timezone):
    user = Users.select().where(Users.chat_id == chat_id).get()
    user.utc_timezone = utc_timezone
    user.save()
    return user

async def update_balance(chat_id, money, add: bool = False, deduct: bool= False):
    try:
        user = Users.select().where(Users.chat_id == chat_id).get()

        if add:
            user.balance = user.balance + money
        if deduct:
            user.balance = user.balance - money

        user.save()
    except peewee.DoesNotExist:
        return None

async def add_user(chat_id, username, referral):
    user = await get_user_by_chat_id(chat_id=chat_id)
    if not user:
        user = Users(
            chat_id=chat_id,
            username=username,
            referral=referral
        )
        user.save()
        return user
    else:
        return user

async def get_user_by_chat_id(chat_id):
    try:
        return Users.select().where(Users.chat_id == chat_id).get()
    except peewee.DoesNotExist:
        return None


async def get_count_users():
    users = Users.select().count()
    return users

async def get_count_user_free_active(free_active: bool = True):
    users = Users.select().where(Users.free_active == free_active).count()
    return users

async def get_count_is_payment(is_payment: bool = True):
    users = Users.select().where(Users.is_payment == is_payment).count()
    return users

async def get_count_referrals_by_chat_id(chat_id):
    users = Users.select().where(Users.referral == chat_id)
    count = 0
    for user in users:
        count += Users.select().where(Users.referral == user.chat_id).count()
    count += users.count()
    return count

async def add_balance_for_all_referrals(chat_id, price):
    user = Users.select().where(Users.chat_id == chat_id).get()
    if user:
        if user.referral:
            await update_balance(user.referral, price * 0.1, True)
            user_2 = Users.select().where(Users.referral == user.referral).get()
            if user_2:
                if user_2.referral:
                    await update_balance(user.referral, price * 0.03, True)


async def update_status_free_active(chat_id, free_active: bool, trial_activate: bool = None):

    if trial_activate:
        return Users.update(free_active=free_active, trial_activate=trial_activate).where(Users.chat_id == chat_id).execute()

    if not trial_activate:
        users = Users.update(free_active=free_active).where(Users.chat_id == chat_id).execute()


async def select_users_free_active(free_active: bool):
    users = Users.select().where(Users.free_active == free_active).execute()
    return users

async def update_status_is_payment(chat_id: int, is_payment: bool):
    user = Users.select().where(Users.chat_id == chat_id).get()
    user.is_payment = is_payment
    user.save()




