from datetime import date

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

import app.api.v1.inventory
from app.core import router
from app.db.schema import get_session
from app.models.inventory import ItemBody
from tests.db.test_schema import get_test_session

client = TestClient(router)
router.dependency_overrides[get_session] = get_test_session


def test_create_and_list_items():
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
