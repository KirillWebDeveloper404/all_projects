from .categories_manuals_model import CategoriesManuals
from .manuals_model import Manuals
from .projects_model import Projects
from .rates_model import Rates
from .settings_model import create_default, Settings
from .shoplist_model import ShopList
from .transactions import Transaction
from .users_model import Users


async def setup_db():
    tables = [Users, CategoriesManuals, Manuals, Settings, Rates, Projects, ShopList, Transaction]
    for table in tables:

        table.create_table()
    await create_default()


