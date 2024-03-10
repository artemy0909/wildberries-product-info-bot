from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from utils.database.config import get_db_url
from .models import Base

engine = create_engine(
    url=get_db_url())

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
