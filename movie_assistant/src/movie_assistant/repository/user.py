from sqlalchemy.orm import Session
from movie_assistant.schemas.user import AddUser, UserBase, GetUser, GetUserInfo
from movie_assistant.models.user import User
from fastapi import HTTPException, status
from movie_assistant.utils.auth import hash_password
from movie_assistant.schemas.app_enums import Role
from movie_assistant.utils.auth import verify_password


class UserRepository:

    @staticmethod
    def add_user(user_info: AddUser, db: Session) -> UserBase:
        user_exists = db.query(User).filter(User.email == user_info.email).first()
        if user_exists:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"User with email {user_info.email} already exists.",
            )
        hashed_password = hash_password(user_info.password)
        new_user = User(
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            email=user_info.email,
            password=hashed_password,
            role=Role.USER.value,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user(user_credentials: GetUser, db: Session) -> GetUserInfo:
        user_exists = (
            db.query(User).filter(User.email == user_credentials.email).first()
        )
        if user_exists is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        if not verify_password(user_credentials.password, user_exists.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        return user_exists
