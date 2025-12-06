from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from movie_assistant.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
