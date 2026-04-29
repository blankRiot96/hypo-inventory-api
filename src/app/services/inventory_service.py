from typing import Sequence

from rapidfuzz import fuzz
from sqlmodel import Session, select

from app.db.schema import Item
from app.models.inventory import ItemBody


def get_items_by_fuzzy_match(session: Session, q: str, limit: int):
    all_items = list(session.exec(select(Item)).all())
    all_items.sort(key=lambda item: fuzz.ratio(item.name, q), reverse=True)
    return all_items[:limit]


def get_item_by_id(session: Session, item_id: int):
    return session.exec(select(Item).filter_by(id=item_id)).first()


def create_item(session: Session, item_body: ItemBody):
    item = Item(
        name=item_body.name,
        price=item_body.price,
        expiry_date=item_body.expiry_date,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def list_items(session: Session) -> Sequence[Item]:
    return session.exec(select(Item)).all()
