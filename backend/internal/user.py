from sqlalchemy import select
from sqlalchemy.orm import Session
#
from backend.database.models import User


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar()
