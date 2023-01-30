import peewee

from .base import BaseModel


class CategoriesManuals(BaseModel):
    name = peewee.TextField()

    class Meta:
        table_name = 'categories_manuals'


async def get_all_categories_manuals():
    return CategoriesManuals.select()

async def create_category_manual(name):
    category = CategoriesManuals(name=name)
    category.save()
    return category


async def get_category_manual_by_id(category_id):
    try:
        return CategoriesManuals.select().where(CategoriesManuals.id == category_id).get()
    except peewee.DoesNotExist:
        return None


async def change_name_category_manuals_by_id(new_name, category_id):
    category = await get_category_manual_by_id(category_id=category_id)
    category.name = new_name
    category.save()
    return category
