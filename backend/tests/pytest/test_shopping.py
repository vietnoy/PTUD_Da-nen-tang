import pytest
from datetime import date, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_shopping_list_success(
    client: AsyncClient, auth_headers, test_group
):
    response = await client.post(
        "/api/v1/shopping/list/",
        json={
            "name": "Weekly Groceries",
            "description": "Shopping for the week",
            "priority": "high",
            "budget": 100.00,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["resultCode"] == "00249"
    assert "shoppingList" in data
    assert data["shoppingList"]["name"] == "Weekly Groceries"
    assert data["shoppingList"]["priority"] == "high"
    assert data["shoppingList"]["status"] == "active"


@pytest.mark.asyncio
async def test_create_shopping_list_with_assignment(
    client: AsyncClient, auth_headers, test_user, test_group
):
    response = await client.post(
        "/api/v1/shopping/list/",
        json={
            "name": "Weekend Shopping",
            "assignToUsername": "testuser",
            "priority": "medium",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["shoppingList"]["assignToUsername"] == "testuser"


@pytest.mark.asyncio
async def test_create_shopping_list_invalid_priority(
    client: AsyncClient, auth_headers, test_group
):
    response = await client.post(
        "/api/v1/shopping/list/",
        json={
            "name": "Test List",
            "priority": "invalid",
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Priority must be" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_shopping_list_user_not_found(
    client: AsyncClient, auth_headers, test_group
):
    response = await client.post(
        "/api/v1/shopping/list/",
        json={
            "name": "Test List",
            "assignToUsername": "nonexistent",
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_shopping_lists(client: AsyncClient, auth_headers, test_group):
    await client.post(
        "/api/v1/shopping/list/",
        json={"name": "List 1", "priority": "high"},
        headers=auth_headers,
    )
    await client.post(
        "/api/v1/shopping/list/",
        json={"name": "List 2", "priority": "low"},
        headers=auth_headers,
    )

    response = await client.get("/api/v1/shopping/list/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00292"
    assert len(data["shoppingLists"]) == 2


@pytest.mark.asyncio
async def test_get_shopping_list_by_id(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_response.json()["shoppingList"]["id"]

    response = await client.post(
        "/api/v1/shopping/list/id/",
        json={"id": list_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["shoppingList"]["id"] == list_id
    assert "tasks" in data
    assert isinstance(data["tasks"], list)


@pytest.mark.asyncio
async def test_update_shopping_list_name(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Old Name", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_response.json()["shoppingList"]["id"]

    response = await client.put(
        "/api/v1/shopping/list/",
        json={"id": list_id, "newName": "New Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00266"
    assert data["shoppingList"]["name"] == "New Name"


@pytest.mark.asyncio
async def test_update_shopping_list_status(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_response.json()["shoppingList"]["id"]

    response = await client.put(
        "/api/v1/shopping/list/",
        json={"id": list_id, "newStatus": "completed"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["shoppingList"]["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_shopping_list(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "To Delete", "priority": "low"},
        headers=auth_headers,
    )
    list_id = create_response.json()["shoppingList"]["id"]

    response = await client.request(
        "DELETE",
        "/api/v1/shopping/list/",
        json={"id": list_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00275"

    get_response = await client.post(
        "/api/v1/shopping/list/id/",
        json={"id": list_id},
        headers=auth_headers,
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_add_tasks_to_list(client: AsyncClient, auth_headers, test_food, test_group):
    create_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_response.json()["shoppingList"]["id"]

    response = await client.post(
        "/api/v1/shopping/task/",
        json={
            "listId": list_id,
            "tasks": [
                {
                    "foodName": "Tomato",
                    "quantity": 2,
                    "unitName": "kg",
                    "estimatedCost": 5.00,
                    "priority": "high",
                },
                {
                    "foodName": "Tomato",
                    "quantity": 1,
                    "estimatedCost": 3.00,
                    "priority": "medium",
                },
            ],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["resultCode"] == "00287"
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["foodName"] == "Tomato"


@pytest.mark.asyncio
async def test_add_task_food_not_found(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_response.json()["shoppingList"]["id"]

    response = await client.post(
        "/api/v1/shopping/task/",
        json={
            "listId": list_id,
            "tasks": [{"foodName": "NonExistent", "quantity": 1, "priority": "low"}],
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_task_mark_done(client: AsyncClient, auth_headers, test_food, test_group):
    create_list_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_list_response.json()["shoppingList"]["id"]

    create_task_response = await client.post(
        "/api/v1/shopping/task/",
        json={
            "listId": list_id,
            "tasks": [{"foodName": "Tomato", "quantity": 2, "priority": "medium"}],
        },
        headers=auth_headers,
    )
    task_id = create_task_response.json()["tasks"][0]["id"]

    response = await client.put(
        "/api/v1/shopping/task/",
        json={"taskId": task_id, "isDone": True, "actualCost": 4.50},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00312"
    assert data["task"]["isDone"] is True
    assert float(data["task"]["actualCost"]) == 4.50
    assert data["task"]["doneAt"] is not None


@pytest.mark.asyncio
async def test_update_task_quantity(client: AsyncClient, auth_headers, test_food, test_group):
    create_list_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_list_response.json()["shoppingList"]["id"]

    create_task_response = await client.post(
        "/api/v1/shopping/task/",
        json={
            "listId": list_id,
            "tasks": [{"foodName": "Tomato", "quantity": 2, "priority": "medium"}],
        },
        headers=auth_headers,
    )
    task_id = create_task_response.json()["tasks"][0]["id"]

    response = await client.put(
        "/api/v1/shopping/task/",
        json={"taskId": task_id, "newQuantity": 5},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["task"]["quantity"]) == 5


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, auth_headers, test_food, test_group):
    create_list_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_list_response.json()["shoppingList"]["id"]

    create_task_response = await client.post(
        "/api/v1/shopping/task/",
        json={
            "listId": list_id,
            "tasks": [{"foodName": "Tomato", "quantity": 2, "priority": "medium"}],
        },
        headers=auth_headers,
    )
    task_id = create_task_response.json()["tasks"][0]["id"]

    response = await client.request(
        "DELETE",
        "/api/v1/shopping/task/",
        json={"taskId": task_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00299"


@pytest.mark.asyncio
async def test_total_cost_calculation(client: AsyncClient, auth_headers, test_food, test_group):
    create_list_response = await client.post(
        "/api/v1/shopping/list/",
        json={"name": "Test List", "priority": "medium"},
        headers=auth_headers,
    )
    list_id = create_list_response.json()["shoppingList"]["id"]

    create_task_response = await client.post(
        "/api/v1/shopping/task/",
        json={
            "listId": list_id,
            "tasks": [
                {"foodName": "Tomato", "quantity": 2, "estimatedCost": 5.00, "priority": "medium"},
                {"foodName": "Tomato", "quantity": 1, "estimatedCost": 3.00, "priority": "low"},
            ],
        },
        headers=auth_headers,
    )
    task1_id = create_task_response.json()["tasks"][0]["id"]

    await client.put(
        "/api/v1/shopping/task/",
        json={"taskId": task1_id, "isDone": True, "actualCost": 6.00},
        headers=auth_headers,
    )

    get_list_response = await client.post(
        "/api/v1/shopping/list/id/",
        json={"id": list_id},
        headers=auth_headers,
    )
    list_data = get_list_response.json()["shoppingList"]
    assert float(list_data["totalCost"]) == 9.00
