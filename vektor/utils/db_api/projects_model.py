from datetime import datetime

import peewee

from .base import BaseTSModel
from .rates_model import Rates
from .users_model import Users, get_user_by_chat_id, update_status_is_payment


class Projects(BaseTSModel):
    bot_token = peewee.TextField(unique=True)
    user = peewee.ForeignKeyField(Users, on_delete='CASCADE')
    name = peewee.TextField()
    rate = peewee.ForeignKeyField(Rates, on_delete='CASCADE')
    is_payment = peewee.BooleanField(default=False)
    end_date = peewee.DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'projects'


async def create_project(token, chat_id, name, rate):
    user = await get_user_by_chat_id(chat_id=chat_id)
    try:
        project = Projects(bot_token=token, user=user.id, name=name, rate=rate)
        project.save()
        return project
    except peewee.IntegrityError:
        return None

async def get_project_by_id(project_id: int):
    return Projects.select().where(Projects.id == project_id).get()


async def change_project_settings(project_id, token=None, name=None, rate=None, is_payment=None, end_date=None):
    project = Projects().select().where(Projects.id == project_id).get()
    if token:
        project.bot_token = token
    if name:
        project.name = name
    if rate:
        project.rate = rate

    if is_payment == False or is_payment == True:
        project.is_payment = is_payment

    if end_date:
        project.end_date = end_date
    project.save()
    return project


async def token_exists(token):
    return Projects.select().where(Projects.bot_token == token)


async def get_project_by_user_chat_id(chat_id):
    user = await get_user_by_chat_id(chat_id=chat_id)
    return Projects.select().where(Projects.user == user.id)


async def get_project_is_not_payment(chat_id, is_payment):
    projects = Projects.select().where((Projects.chat_id == chat_id) &
                                       (Projects.is_payment == is_payment)).get()
    return projects


async def get_all_projects():
    projects = Projects.select().execute()
    return projects

async def delete_project_by_id(project_id):
    project = Projects.select().where(Projects.id == project_id).get()
    project.delete_instance()
