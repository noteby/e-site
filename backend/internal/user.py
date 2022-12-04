from datetime import datetime
#
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
#
from backend.database.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session, email: str, password: str) -> User:
    user = User(email=email, hashed_password=get_password_hash(password),
                created_at=datetime.now()
                )
    db.add(user)
    db.commit()

    return user


def create_user_by_manual(email: str, password: str):
    from backend.database.engine import SessionLocal
    db: Session = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if user:
            logger.warning(f'User already exist, id:{user.id}')
        else:
            user = create_user(db, email, password)
            logger.info(f'Create user, id:{user.id}')
    finally:
        db.close()
