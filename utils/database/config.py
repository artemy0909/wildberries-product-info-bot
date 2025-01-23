from utils.config import Config


def get_db_url():
    return (
        f"postgresql+asyncpg://{Config.DB_USER}:{Config.DB_PASS}"
        f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
    )
