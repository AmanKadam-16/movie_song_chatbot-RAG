from movie_assistant.repository.user import UserRepository
from movie_assistant.schemas import user as user_schema
from sqlalchemy.orm import Session


def register_user(user_info: user_schema.AddUser, db: Session) -> user_schema.UserBase:
    user_added = UserRepository.add_user(user_info=user_info, db=db)
    return user_added


def get_user_info(
    user_credentials: user_schema.GetUser, db: Session
) -> user_schema.GetUserInfo:
    user_info = UserRepository.get_user(user_credentials=user_credentials, db=db)
    return user_info
