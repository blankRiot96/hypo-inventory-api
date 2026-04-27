from app.core import router
from app.db.schema import Item, SessionDep
from app.models.inventory import ItemBody
from app.services import inventory_service


@router.post("/items/")
async def create_item(session: SessionDep, body: ItemBody):
    item = Item(name=body.name, price=body.price, expiry_date=body.expiry_date)
    return inventory_service.create_item(session, item)


@router.get("/items/")
async def get_items(session: SessionDep):
    return inventory_service.list_items(session)
