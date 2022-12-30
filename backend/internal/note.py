from datetime import datetime
#
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session
#
from backend.database.models import Note


def create_note(db: Session, title: str, display: bool, content: str) -> Note:
    note = Note(
        title=title, display=display, content=content,
        created_at=datetime.now()
    )
    db.add(note)
    db.commit()

    return note


def update_note(db: Session, note_id: int, title: str, display: bool, content: str) -> Note:
    stmt = (
        update(Note)
        .where(Note.id == note_id)
        .values(title=title, display=display, content=content, updated_at=datetime.now())
        .returning(Note)
    )
    note = db.execute(stmt).scalar()
    db.commit()

    return note


def get_note_by_id(db: Session, note_id: int, display: bool = None) -> Note | None:
    stmt = select(Note).where(Note.id == note_id)
    if display is not None:
        stmt = stmt.where(Note.display == display)

    return db.execute(stmt).scalar()


def get_note_list(db: Session, display: bool = None, limit: int = 8, offset: int = 0):
    stmt = select(Note).limit(limit).offset(offset).order_by(Note.created_at.desc())
    if display is not None:
        stmt = stmt.where(Note.display == display)

    return db.execute(stmt).scalars()


def get_note_count(db: Session, display: bool = None):
    query = db.query(func.count(Note.id))
    if display is not None:
        query = query.where(Note.display == display)

    return query.scalar()
