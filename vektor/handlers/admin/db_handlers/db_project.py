from peewee import PostgresqlDatabase


async def connect_db_project(db_name: str, db_user: str, db_password: str, db_port: int = 5432, db_host: str = "localhost"):
    db_handler = PostgresqlDatabase(
        db_name, host=db_host, port=db_port, user=db_user, password=db_password
    )
    return db_handler

