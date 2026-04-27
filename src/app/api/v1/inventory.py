from typing import Annotated

from fastapi import Query

from app.core import router
from app.db.schema import Item, SessionDep
from app.models.inventory import ItemBody
from app.services import inventory_service


@router.get("/items/fuzzy/")
async def get_items_by_fuzzy_name(
    session: SessionDep,
    q: Annotated[str, Query],
    limit: Annotated[int, Query(gt=0)] = 5,
):
    return inventory_service.get_items_by_fuzzy_match(session, q, limit)


@router.get("/items/{item_id}")
async def get_item_by_id(session: SessionDep, item_id: int):
    return inventory_service.get_item_by_id(session, item_id)


@router.post("/items/")
async def create_item(session: SessionDep, body: ItemBody):
    return inventory_service.create_item(session, body)


@router.get("/items/")
async def get_items(session: SessionDep):
    return inventory_service.list_items(session)
