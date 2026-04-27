from dataclasses import replace
from datetime import date

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

import app.api.v1.inventory
from app.models.inventory import ItemBody

test_item_body = jsonable_encoder(
    ItemBody(
        name="golden pan",
        price=1000,
        expiry_date=date(year=3000, month=10, day=12),
    )
)


def test_create_and_list_items(client: TestClient):
    response = client.post("/items/", json=test_item_body)
    assert response.status_code == 200

    response = client.get("/items/")
    assert len(response.json()) == 1


def test_get_item_by_id(client: TestClient):
    response = client.post("/items/", json=test_item_body)
    assert response.status_code == 200
    target = response.json()

    response = client.get(f"/items/{target['id']}")
    assert response.json() == target


def test_item_id_generation(client: TestClient):
    for i in range(10):
        response = client.post("/items/", json=test_item_body)
        assert response.status_code == 200
        assert response.json()["id"] == i

    response = client.get("/items/")
    assert len(response.json()) == 10


def test_fresh_db(client: TestClient):
    response = client.get("/items/")
    assert len(response.json()) == 0


def test_fuzzy_match(client: TestClient):
    item_names = (
        "banana",
        "knife",
        "cat in a box",
        "pandora's box",
        "silver spoon",
        "pan",
        "golf club",
    )

    item_body_schema = ItemBody(name="", price=1000, expiry_date=date(2027, 1, 1))
    for name in item_names:
        item_body = item_body_schema.model_copy()
        item_body.name = name
        response = client.post("/items/", json=jsonable_encoder(item_body))
        assert response.status_code == 200

    response = client.get("/items/fuzzy/", params={"q": "pan", "limit": 3})
    assert [obj["name"] for obj in response.json()] == [
        "pan",
        "banana",
        "pandora's box",
    ]
