import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_recipe_success(client: AsyncClient, auth_headers, test_group):
    response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Tomato Salad",
            "description": "Fresh tomato salad recipe",
            "htmlContent": "<p>Mix tomatoes with olive oil</p>",
            "prepTimeMinutes": 10,
            "cookTimeMinutes": 0,
            "servings": 4,
            "difficulty": "easy",
            "isPublic": False,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["resultCode"] == "00357"
    assert "recipe" in data
    assert data["recipe"]["name"] == "Tomato Salad"
    assert data["recipe"]["difficulty"] == "easy"


@pytest.mark.asyncio
async def test_create_recipe_with_food(client: AsyncClient, auth_headers, test_food, test_group):
    response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Tomato Dish",
            "description": "Tomato-based recipe",
            "htmlContent": "<p>Cook tomatoes</p>",
            "foodName": "Tomato",
            "difficulty": "medium",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["recipe"]["foodName"] == "Tomato"


@pytest.mark.asyncio
async def test_create_recipe_invalid_difficulty(client: AsyncClient, auth_headers, test_group):
    response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Test Recipe",
            "description": "Test description",
            "htmlContent": "<p>Test content</p>",
            "difficulty": "invalid",
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Difficulty must be" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_recipes(client: AsyncClient, auth_headers, test_group):
    await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Recipe 1",
            "description": "Description 1",
            "htmlContent": "<p>Content 1</p>",
            "difficulty": "easy",
        },
        headers=auth_headers,
    )

    await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Recipe 2",
            "description": "Description 2",
            "htmlContent": "<p>Content 2</p>",
            "difficulty": "hard",
        },
        headers=auth_headers,
    )

    response = await client.get("/api/v1/recipes/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00378"
    assert len(data["recipes"]) == 2


@pytest.mark.asyncio
async def test_get_recipe_by_id(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Test Recipe",
            "description": "Test description",
            "htmlContent": "<p>Test content</p>",
        },
        headers=auth_headers,
    )
    recipe_id = create_response.json()["recipe"]["id"]

    response = await client.post(
        "/api/v1/recipes/id/",
        json={"id": recipe_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["recipe"]["id"] == recipe_id
    assert data["recipe"]["htmlContent"] == "<p>Test content</p>"


@pytest.mark.asyncio
async def test_update_recipe_name(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Old Name",
            "description": "Description",
            "htmlContent": "<p>Content</p>",
        },
        headers=auth_headers,
    )
    recipe_id = create_response.json()["recipe"]["id"]

    response = await client.put(
        "/api/v1/recipes/",
        data={
            "id": recipe_id,
            "newName": "New Name",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00370"
    assert data["recipe"]["name"] == "New Name"


@pytest.mark.asyncio
async def test_update_recipe_html_content(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Test Recipe",
            "description": "Description",
            "htmlContent": "<p>Old content</p>",
        },
        headers=auth_headers,
    )
    recipe_id = create_response.json()["recipe"]["id"]

    response = await client.put(
        "/api/v1/recipes/",
        data={
            "id": recipe_id,
            "newHtmlContent": "<p>New content</p>",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["recipe"]["htmlContent"] == "<p>New content</p>"


@pytest.mark.asyncio
async def test_update_recipe_difficulty(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Test Recipe",
            "description": "Description",
            "htmlContent": "<p>Content</p>",
            "difficulty": "easy",
        },
        headers=auth_headers,
    )
    recipe_id = create_response.json()["recipe"]["id"]

    response = await client.put(
        "/api/v1/recipes/",
        data={
            "id": recipe_id,
            "newDifficulty": "hard",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["recipe"]["difficulty"] == "hard"


@pytest.mark.asyncio
async def test_delete_recipe(client: AsyncClient, auth_headers, test_group):
    create_response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "To Delete",
            "description": "Will be deleted",
            "htmlContent": "<p>Content</p>",
        },
        headers=auth_headers,
    )
    recipe_id = create_response.json()["recipe"]["id"]

    response = await client.request(
        "DELETE",
        "/api/v1/recipes/",
        json={"id": recipe_id},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["resultCode"] == "00376"

    get_response = await client.post(
        "/api/v1/recipes/id/",
        json={"id": recipe_id},
        headers=auth_headers,
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_recipe_with_timing(client: AsyncClient, auth_headers, test_group):
    response = await client.post(
        "/api/v1/recipes/",
        data={
            "name": "Timed Recipe",
            "description": "Recipe with timing",
            "htmlContent": "<p>Cook for specified time</p>",
            "prepTimeMinutes": 15,
            "cookTimeMinutes": 30,
            "servings": 6,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["recipe"]["prepTimeMinutes"] == 15
    assert data["recipe"]["cookTimeMinutes"] == 30
    assert data["recipe"]["servings"] == 6


@pytest.mark.asyncio
async def test_recipe_not_found(client: AsyncClient, auth_headers, test_group):
    response = await client.post(
        "/api/v1/recipes/id/",
        json={"id": 99999},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_recipe_not_found(client: AsyncClient, auth_headers, test_group):
    response = await client.put(
        "/api/v1/recipes/",
        data={
            "id": 99999,
            "newName": "New Name",
        },
        headers=auth_headers,
    )
    assert response.status_code == 404
