import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class __Config:
    TOKEN = os.getenv("BOT_TOKEN")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASS = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_NAME")
    ARTICLE_UPDATE_INTERVAL = int(os.getenv("ARTICLE_UPDATE_INTERVAL"))
    SUBSCRIBE_PUSH_INTERVAL = int(os.getenv("SUBSCRIBE_PUSH_INTERVAL"))
    API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN", "")


Config = __Config()
