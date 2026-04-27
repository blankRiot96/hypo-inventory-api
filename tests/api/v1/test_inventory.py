from datetime import date

from fastapi.encoders import jsonable_encoder

import app.api.v1.inventory
from app.models.inventory import ItemBody


def test_create_and_list_items(client):
    response = client.post(
        "/items/",
        json=jsonable_encoder(
            ItemBody(
                name="golden pan",
                price=1000,
                expiry_date=date(year=3000, month=10, day=12),
            )
        ),
    )
    assert response.status_code == 200

    response = client.get("/items/")
    assert len(response.json()) == 1
