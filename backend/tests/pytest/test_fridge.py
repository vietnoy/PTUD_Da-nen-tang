import pytest
from datetime import date, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_fridge_item_success(
    client: AsyncClient, auth_headers, test_food
):
    response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2.5,
            "useWithinDate": str(date.today() + timedelta(days=7)),
            "location": "fridge",
            "cost": 5.99,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["resultCode"] == "00202"
    assert "fridgeItem" in data
    assert float(data["fridgeItem"]["quantity"]) == 2.5
    assert data["fridgeItem"]["foodName"] == "Tomato"
    assert data["fridgeItem"]["location"] == "fridge"


@pytest.mark.asyncio
async def test_create_fridge_item_food_not_found(
    client: AsyncClient, auth_headers, test_food
):
    response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "NonExistentFood",
            "quantity": 1,
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Food not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_fridge_item_no_group(client: AsyncClient, db_session):
    from app.models import User
    from app.core.security import create_access_token

    user_no_group = User(
        email="nogroup@example.com",
        password_hash="hashed_password",
        name="No Group User",
        username="nogroupuser",
        language="en",
        timezone=0,
        is_active=True,
        is_verified=True,
    )
    db_session.add(user_no_group)
    db_session.commit()
    db_session.refresh(user_no_group)

    token = create_access_token({"sub": str(user_no_group.id)})
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 1,
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=headers,
    )
    assert response.status_code == 400
    assert "not in any group" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_fridge_items(client: AsyncClient, auth_headers, test_food):
    await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2,
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=auth_headers,
    )

    await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 3,
            "useWithinDate": str(date.today() + timedelta(days=5)),
            "location": "freezer",
        },
        headers=auth_headers,
    )

    response = await client.get("/api/v1/fridge/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00228"
    assert "fridgeItems" in data
    assert len(data["fridgeItems"]) == 2


@pytest.mark.asyncio
async def test_get_fridge_item_by_id_success(
    client: AsyncClient, auth_headers, test_food
):
    create_response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2,
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["fridgeItem"]["id"]

    response = await client.post(
        "/api/v1/fridge/id/",
        json={"id": item_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00237"
    assert data["fridgeItem"]["id"] == item_id


@pytest.mark.asyncio
async def test_get_fridge_item_by_id_not_found(client: AsyncClient, auth_headers, test_group):
    response = await client.post(
        "/api/v1/fridge/id/",
        json={"id": 99999},
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_fridge_item_quantity(client: AsyncClient, auth_headers, test_food):
    create_response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2,
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["fridgeItem"]["id"]

    response = await client.put(
        "/api/v1/fridge/",
        json={"id": item_id, "newQuantity": 5.5},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00216"
    assert float(data["fridgeItem"]["quantity"]) == 5.5


@pytest.mark.asyncio
async def test_update_fridge_item_mark_opened(
    client: AsyncClient, auth_headers, test_food
):
    create_response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2,
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["fridgeItem"]["id"]

    response = await client.put(
        "/api/v1/fridge/",
        json={"id": item_id, "isOpened": True},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fridgeItem"]["isOpened"] is True
    assert data["fridgeItem"]["openedAt"] is not None


@pytest.mark.asyncio
async def test_update_fridge_item_location(client: AsyncClient, auth_headers, test_food):
    create_response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2,
            "useWithinDate": str(date.today() + timedelta(days=7)),
            "location": "fridge",
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["fridgeItem"]["id"]

    response = await client.put(
        "/api/v1/fridge/",
        json={"id": item_id, "newLocation": "freezer"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fridgeItem"]["location"] == "freezer"


@pytest.mark.asyncio
async def test_update_fridge_item_not_found(client: AsyncClient, auth_headers, test_group):
    response = await client.put(
        "/api/v1/fridge/",
        json={"id": 99999, "newQuantity": 5},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_fridge_item_success(client: AsyncClient, auth_headers, test_food):
    create_response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2,
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=auth_headers,
    )
    item_id = create_response.json()["fridgeItem"]["id"]

    response = await client.request(
        "DELETE",
        "/api/v1/fridge/",
        json={"id": item_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00224"

    get_response = await client.post(
        "/api/v1/fridge/id/",
        json={"id": item_id},
        headers=auth_headers,
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_fridge_item_not_found(client: AsyncClient, auth_headers, test_group):
    response = await client.request(
        "DELETE",
        "/api/v1/fridge/",
        json={"id": 99999},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_fridge_item_with_unit(
    client: AsyncClient, auth_headers, test_food, test_unit
):
    response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2.5,
            "unitName": "kg",
            "useWithinDate": str(date.today() + timedelta(days=7)),
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["fridgeItem"]["unitName"] == "kg"


@pytest.mark.asyncio
async def test_fridge_item_with_note(client: AsyncClient, auth_headers, test_food):
    response = await client.post(
        "/api/v1/fridge/",
        json={
            "foodName": "Tomato",
            "quantity": 2,
            "useWithinDate": str(date.today() + timedelta(days=7)),
            "note": "Bought from farmers market",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["fridgeItem"]["note"] == "Bought from farmers market"
