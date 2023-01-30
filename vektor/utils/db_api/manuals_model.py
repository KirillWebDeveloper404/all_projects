import peewee

from utils.db_api.base import BaseModel
from utils.db_api.categories_manuals_model import CategoriesManuals


class Manuals(BaseModel):
    category = peewee.ForeignKeyField(CategoriesManuals, on_delete='CASCADE')
    name = peewee.TextField()
    desc = peewee.TextField()

    class Meta:
        table_name = 'manuals'


async def delete_manual_by_id(manual_id):
    manual = await get_manual_by_id(manual_id)
    manual.delete_instance()


async def get_all_manuals_by_category_id(category_id):
    return Manuals.select().where(Manuals.category == category_id)


async def create_manual(category_id, name, desc):
    manual = Manuals(category=category_id, name=name, desc=desc)
    manual.save()
    return manual


async def get_manual_by_id(manual_id):
    try:
        return Manuals.select().where(Manuals.id == manual_id).get()
    except peewee.DoesNotExist:
        return None


async def change_manual_by_id(manual_id, name=None, desc=None, category_id=None):
    manual = await get_manual_by_id(manual_id=manual_id)
    if category_id:
        manual.category = category_id
    if name:
        manual.name = name
    if desc:
        manual.desc = desc
    manual.save()
    return manual
