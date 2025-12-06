from sqlalchemy.orm import Session
from movie_assistant.database.deps import get_db
from movie_assistant.models.user import User
from movie_assistant.schemas.app_enums import Role
from movie_assistant.core.config import settings
from movie_assistant.utils.auth import hash_password


def seed_admin():
    db: Session = next(get_db())
    admin_email = settings.ADMIN_EMAIL
    admin_password = hash_password(settings.ADMIN_PASSWORD)
    admin_exists = db.query(User).filter(User.role == Role.ADMIN.value).first()
    if admin_exists:
        return "Admin Already Exists."
    new_admin = User(
        first_name="admin",
        last_name="admin",
        email=admin_email,
        password=admin_password,
        role=Role.ADMIN.value,
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return "Admin Seeded Successfully."
