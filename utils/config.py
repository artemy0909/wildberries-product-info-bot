from dataclasses import dataclass

from dotenv import load_dotenv
from os import getenv

load_dotenv()


@dataclass
class Config:
    TOKEN = getenv("BOT_TOKEN")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_USER = getenv("DB_USER")
    DB_PASS = getenv("DB_PASS")
    DB_NAME = getenv("DB_NAME")
