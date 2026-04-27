from typing import Sequence

from sqlmodel import Session, select

from app.db.schema import Item


def create_item(session: Session, item: Item):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def list_items(session: Session) -> Sequence[Item]:
    return session.exec(select(Item)).all()
