from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Entry

def create_entry_record(
    db: Session,
    content: str,
    ai_result: dict,
) -> Entry:
    entry = Entry(
        content=content,
        entry_type=ai_result["entry_type"],
        chinese_meaning=ai_result["chinese_meaning"],
        explanation=ai_result["explanation"],
        part_of_speech=ai_result["part_of_speech"],
        familiarity_level=0,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_entry_records(db: Session) -> list[Entry]:
    statement = select(Entry).order_by(Entry.id.desc())

    result = db.execute(statement)

    return list(result.scalars().all())

def get_entry_record(
    db: Session,
    entry_id: int,
) -> Entry | None:
    return db.get(Entry, entry_id)

def update_entry_record(
    db: Session,
    entry_id: int,
    update_data: dict,
) -> Entry | None:
    entry = db.get(Entry, entry_id)

    if entry is None:
        return None

    for field, value in update_data.items():
        setattr(entry, field, value)

    db.commit()
    db.refresh(entry)

    return entry


def delete_entry_record(
    db: Session,
    entry_id: int,
) -> Entry | None:
    entry = db.get(Entry, entry_id)

    if entry is None:
        return None

    db.delete(entry)
    db.commit()

    return entry