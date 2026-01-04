import pytest
from datetime import date, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_meal_plan_success(client: AsyncClient, auth_headers, test_food):
    response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "breakfast",
            "mealDate": str(date.today()),
            "servingSize": 2.5,
            "unitName": "kg",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["resultCode"] == "00322"
    assert "mealPlan" in data
    assert data["mealPlan"]["mealType"] == "breakfast"
    assert data["mealPlan"]["foodName"] == "Tomato"


@pytest.mark.asyncio
async def test_create_meal_plan_invalid_meal_type(
    client: AsyncClient, auth_headers, test_food
):
    response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "snack",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Meal type must be" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_meal_plan_food_not_found(client: AsyncClient, auth_headers, test_group):
    response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "NonExistent",
            "mealType": "lunch",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_meal_plans(client: AsyncClient, auth_headers, test_food):
    await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "breakfast",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )

    await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "lunch",
            "mealDate": str(date.today() + timedelta(days=1)),
        },
        headers=auth_headers,
    )

    response = await client.get("/api/v1/meal-plans/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00348"
    assert len(data["mealPlans"]) == 2


@pytest.mark.asyncio
async def test_get_meal_plans_with_date_filter(
    client: AsyncClient, auth_headers, test_food
):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "breakfast",
            "mealDate": str(today),
        },
        headers=auth_headers,
    )

    await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "lunch",
            "mealDate": str(tomorrow),
        },
        headers=auth_headers,
    )

    response = await client.get(
        f"/api/v1/meal-plans/?start_date={str(today)}&end_date={str(today)}",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["mealPlans"]) == 1
    assert data["mealPlans"][0]["mealDate"] == str(today)


@pytest.mark.asyncio
async def test_get_meal_plans_by_meal_type(
    client: AsyncClient, auth_headers, test_food
):
    await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "breakfast",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )

    await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "lunch",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )

    response = await client.get(
        "/api/v1/meal-plans/?meal_type=breakfast", headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert all(mp["mealType"] == "breakfast" for mp in data["mealPlans"])


@pytest.mark.asyncio
async def test_get_meal_plan_by_id(client: AsyncClient, auth_headers, test_food):
    create_response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "dinner",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    meal_plan_id = create_response.json()["mealPlan"]["id"]

    response = await client.post(
        "/api/v1/meal-plans/id/",
        json={"id": meal_plan_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mealPlan"]["id"] == meal_plan_id


@pytest.mark.asyncio
async def test_update_meal_plan_food(client: AsyncClient, auth_headers, test_food):
    create_response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "breakfast",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    meal_plan_id = create_response.json()["mealPlan"]["id"]

    response = await client.put(
        "/api/v1/meal-plans/",
        json={"id": meal_plan_id, "newFoodName": "Tomato"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00344"


@pytest.mark.asyncio
async def test_update_meal_plan_mark_prepared(
    client: AsyncClient, auth_headers, test_food
):
    create_response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "lunch",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    meal_plan_id = create_response.json()["mealPlan"]["id"]

    response = await client.put(
        "/api/v1/meal-plans/",
        json={"id": meal_plan_id, "isPrepared": True},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mealPlan"]["isPrepared"] is True
    assert data["mealPlan"]["preparedAt"] is not None


@pytest.mark.asyncio
async def test_update_meal_plan_meal_type(client: AsyncClient, auth_headers, test_food):
    create_response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "breakfast",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    meal_plan_id = create_response.json()["mealPlan"]["id"]

    response = await client.put(
        "/api/v1/meal-plans/",
        json={"id": meal_plan_id, "newMealType": "dinner"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mealPlan"]["mealType"] == "dinner"


@pytest.mark.asyncio
async def test_delete_meal_plan(client: AsyncClient, auth_headers, test_food):
    create_response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "breakfast",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    meal_plan_id = create_response.json()["mealPlan"]["id"]

    response = await client.request(
        "DELETE",
        "/api/v1/meal-plans/",
        json={"id": meal_plan_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00330"

    get_response = await client.post(
        "/api/v1/meal-plans/id/",
        json={"id": meal_plan_id},
        headers=auth_headers,
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_meal_plan_case_insensitive_meal_type(
    client: AsyncClient, auth_headers, test_food
):
    response = await client.post(
        "/api/v1/meal-plans/",
        json={
            "foodName": "Tomato",
            "mealType": "BREAKFAST",
            "mealDate": str(date.today()),
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["mealPlan"]["mealType"] == "breakfast"
