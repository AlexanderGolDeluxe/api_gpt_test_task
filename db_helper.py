from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DB_URL, DEBUG_MODE
from models import Base


class DatabaseHelper:

    @logger.catch
    def __init__(self, db_url: str, echo_mode: bool):
        self.engine = create_engine(
            url=db_url, echo=echo_mode
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )
        self.db_session = scoped_session(self.session_factory)
        self.__init_db()

    @logger.catch
    def __init_db(self):
        Base.metadata.create_all(bind=self.engine)


db_helper = DatabaseHelper(db_url=DB_URL, echo_mode=DEBUG_MODE)
