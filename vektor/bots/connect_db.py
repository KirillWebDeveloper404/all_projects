# from admin_panel.database.commands.DATABASE import DatabaseBot
# from data.config import DB_USER, DB_PASS, DB_HOST
# from loader import database_bots
# from utils.db_api.projects_model import get_all_projects
#
#
# async def connect_databases_bots():
#     projects = await get_all_projects()
#     for project in projects:
#         database = DatabaseBot()
#         await database.connect_db(dbname=f"project_{project.id}",
#                                   user=DB_USER, password=DB_PASS,
#                                   host=DB_HOST)
#         database_bots[project.id] = database
