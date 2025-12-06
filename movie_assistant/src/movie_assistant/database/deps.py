from movie_assistant.database.database import SessionLocal
from typing import Generator
from sqlalchemy.orm import Session


def get_db() -> Generator:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
