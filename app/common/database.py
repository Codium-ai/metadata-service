""" Database module for the service """

from app.common.config import settings
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# keeps all metadata about the DB schema, shared for all entities
Base = declarative_base()

# Create an inspector instance
inspector = inspect(engine)


def get_db():
    """
    generator function that provides a new database session for each request
    and  ensures that the session is properly closed after use
    """
    # create a new db session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
