from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.database.config import get_db_url
from .models import Base

engine = create_engine(
    url=get_db_url())

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
