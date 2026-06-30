from config import Config
from database.base import DatabaseAdapter
from database.mariadb_adapter import MariaDBAdapter
from database.sqlite_adapter import SQLiteAdapter


def create_database_adapter(config: Config) -> DatabaseAdapter:
  db_type = config.DB_TYPE

  if db_type == "sqlite":
    return SQLiteAdapter(config.SQLITE_PATH)

  if db_type == "mariadb":
    return MariaDBAdapter(
      host=config.MARIADB_HOST,
      port=config.MARIADB_PORT,
      user=config.MARIADB_USER,
      password=config.MARIADB_PASSWORD,
      database=config.MARIADB_DATABASE,
    )

  raise ValueError(f"Unsupported database type: {db_type}")
