from dataclasses import dataclass

from dotenv import load_dotenv
from os import getenv

load_dotenv()


@dataclass
class Config:
    TOKEN = getenv("BOT_TOKEN")
    DB_HOST = getenv("POSTGRES_HOST")
    DB_PORT = getenv("POSTGRES_PORT")
    DB_USER = getenv("POSTGRES_USER")
    DB_PASS = getenv("POSTGRES_PASSWORD")
    DB_NAME = getenv("POSTGRES_NAME")
