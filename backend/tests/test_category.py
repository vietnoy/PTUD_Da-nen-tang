"""Tests for Category API endpoints and service functionality."""

from unittest.mock import Mock, patch

import pytest
from app.core.deps import get_current_user, get_db
from app.main import app
from app.models import Category, User
from app.schemas import (
    AddCategoryRequest,
    AddCategoryResponse,
    DeleteCategoryRequest,
    DeleteCategoryResponse,
    EditCategoryRequest,
    EditCategoryResponse,
    GetAllCategoriesResponse,
)
from app.services.category import CategoryService
from app.utils.responseCodeEnums import ResponseCode
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Test client setup
client = TestClient(app)


class TestCategoryService:
    """Unit tests for CategoryService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock(spec=Session)

    @pytest.fixture
    def sample_category(self):
        """Create a sample category for testing."""
        category = Mock(spec=Category)
        category.id = 1
        category.name = "Vegetables"
        category.description = "Fresh vegetables"
        category.created_at = "2023-01-01T00:00:00Z"
        category.updated_at = "2023-01-01T00:00:00Z"
        return category

    def test_add_category_success(self, mock_db, sample_category):
        """Test successful category creation."""
        # Arrange
        request = AddCategoryRequest(name="Vegetables", description="Fresh vegetables")
        mock_db.query().filter().first.return_value = None  # No existing category
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Mock the new category creation
        with patch("app.services.category.Category", return_value=sample_category):
            # Act
            result = CategoryService.add_category(mock_db, request)

            # Assert
            assert isinstance(result, AddCategoryResponse)
            assert result.result_code == ResponseCode.CREATE_CATEGORY_SUCCESS.value[0]
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()

    def test_add_category_already_exists(self, mock_db, sample_category):
        """Test category creation when category already exists."""
        # Arrange
        request = AddCategoryRequest(name="Vegetables", description="Fresh vegetables")
        mock_db.query().filter().first.return_value = (
            sample_category  # Existing category
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            CategoryService.add_category(mock_db, request)

        # The exact exception depends on CategoryService implementation

    def test_get_all_categories_success(self, mock_db):
        """Test successful retrieval of all categories."""
        # Arrange
        categories = [
            Mock(
                id=1,
                name="Vegetables",
                description="Fresh vegetables",
                created_at="2023-01-01T00:00:00Z",
            ),
            Mock(
                id=2,
                name="Fruits",
                description="Fresh fruits",
                created_at="2023-01-02T00:00:00Z",
            ),
        ]
        mock_query = Mock()
        mock_query.all.return_value = categories
        mock_db.query.return_value = mock_query

        # Act
        result = CategoryService.get_all_categories(mock_db)

        # Assert
        assert isinstance(result, GetAllCategoriesResponse)
        assert len(result.categories) == 2
        assert result.result_code == ResponseCode.GET_CATEGORIES_SUCCESS.value[0]

    def test_edit_category_success(self, mock_db, sample_category):
        """Test successful category editing."""
        # Arrange
        request = EditCategoryRequest(oldName="Vegetables", newName="Fresh Vegetables")
        mock_db.query().filter().first.return_value = sample_category
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Act
        result = CategoryService.edit_category(mock_db, request)

        # Assert
        assert isinstance(result, EditCategoryResponse)
        assert sample_category.name == "Fresh Vegetables"
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_delete_category_success(self, mock_db, sample_category):
        """Test successful category deletion."""
        # Arrange
        request = DeleteCategoryRequest(name="Vegetables")
        mock_db.query().filter().first.return_value = sample_category
        mock_db.delete = Mock()
        mock_db.commit = Mock()

        # Act
        result = CategoryService.delete_category(mock_db, request)

        # Assert
        assert isinstance(result, DeleteCategoryResponse)
        mock_db.delete.assert_called_once_with(sample_category)
        mock_db.commit.assert_called_once()


class TestCategoryAPI:
    """Integration tests for Category API endpoints."""

    @pytest.fixture
    def mock_admin_user(self):
        """Create a mock admin user."""
        user = Mock(spec=User)
        user.id = 1
        user.email = "admin@example.com"
        user.is_admin = True
        user.is_active = True
        return user

    @pytest.fixture
    def mock_regular_user(self):
        """Create a mock regular user."""
        user = Mock(spec=User)
        user.id = 2
        user.email = "user@example.com"
        user.is_admin = False
        user.is_active = True
        return user

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session."""
        return Mock(spec=Session)

    def test_add_category_success_as_admin(self, mock_admin_user, mock_db_session):
        """Test adding category as admin user."""

        # Arrange
        def override_get_current_user():
            return mock_admin_user

        def override_get_db():
            yield mock_db_session

        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

        category_data = {"name": "Vegetables", "description": "Fresh vegetables"}

        with patch.object(CategoryService, "add_category") as mock_add:
            mock_response = AddCategoryResponse(
                resultMessage={"en": "Success", "vn": "Thành công"}, resultCode="00135"
            )
            mock_add.return_value = mock_response

            # Act
            response = client.post("/categories/", json=category_data)

            # Assert
            assert response.status_code == 200
            mock_add.assert_called_once()

        # Cleanup
        app.dependency_overrides.clear()

    def test_add_category_forbidden_as_regular_user(
        self, mock_regular_user, mock_db_session
    ):
        """Test adding category as regular user (should fail)."""

        # Arrange
        def override_get_current_user():
            return mock_regular_user

        def override_get_db():
            yield mock_db_session

        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

        category_data = {"name": "Vegetables", "description": "Fresh vegetables"}

        # Act
        response = client.post("/categories/", json=category_data)

        # Assert
        assert response.status_code == 403
        assert "Admin privileges required" in response.json()["detail"]

        # Cleanup
        app.dependency_overrides.clear()

    def test_get_all_categories_success(self, mock_db_session):
        """Test getting all categories (no auth required)."""

        # Arrange
        def override_get_db():
            yield mock_db_session

        app.dependency_overrides[get_db] = override_get_db

        with patch.object(CategoryService, "get_all_categories") as mock_get_all:
            mock_response = GetAllCategoriesResponse(
                categories=[],
                resultMessage={"en": "Success", "vn": "Thành công"},
                resultCode="00129",
            )
            mock_get_all.return_value = mock_response

            # Act
            response = client.get("/categories/")

            # Assert
            assert response.status_code == 200
            mock_get_all.assert_called_once()

        # Cleanup
        app.dependency_overrides.clear()

    def test_edit_category_success_as_admin(self, mock_admin_user, mock_db_session):
        """Test editing category as admin user."""

        # Arrange
        def override_get_current_user():
            return mock_admin_user

        def override_get_db():
            yield mock_db_session

        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

        category_data = {"oldName": "Vegetables", "newName": "Fresh Vegetables"}

        with patch.object(CategoryService, "edit_category") as mock_edit:
            mock_response = EditCategoryResponse(
                resultMessage={"en": "Success", "vn": "Thành công"}, resultCode="00122"
            )
            mock_edit.return_value = mock_response

            # Act
            response = client.put("/categories/", json=category_data)

            # Assert
            assert response.status_code == 200
            mock_edit.assert_called_once()

        # Cleanup
        app.dependency_overrides.clear()

    def test_delete_category_success_as_admin(self, mock_admin_user, mock_db_session):
        """Test deleting category as admin user."""

        # Arrange
        def override_get_current_user():
            return mock_admin_user

        def override_get_db():
            yield mock_db_session

        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

        category_data = {"name": "Vegetables"}

        with patch.object(CategoryService, "delete_category") as mock_delete:
            mock_response = DeleteCategoryResponse(
                resultMessage={"en": "Success", "vn": "Thành công"}, resultCode="00128"
            )
            mock_delete.return_value = mock_response

            # Act
            response = client.delete("/categories/", json=category_data)

            # Assert
            assert response.status_code == 200
            mock_delete.assert_called_once()

        # Cleanup
        app.dependency_overrides.clear()

    def test_delete_category_forbidden_as_regular_user(
        self, mock_regular_user, mock_db_session
    ):
        """Test deleting category as regular user (should fail)."""

        # Arrange
        def override_get_current_user():
            return mock_regular_user

        def override_get_db():
            yield mock_db_session

        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db

        category_data = {"name": "Vegetables"}

        # Act
        response = client.delete("/categories/", json=category_data)

        # Assert
        assert response.status_code == 403
        assert "Admin privileges required" in response.json()["detail"]

        # Cleanup
        app.dependency_overrides.clear()


@pytest.mark.asyncio
class TestCategoryAPIAsync:
    """Async integration tests for Category API."""

    async def test_add_category_async(self):
        """Test async category creation."""
        from httpx import AsyncClient

        async with AsyncClient(app=app, base_url="http://test") as ac:
            # This would require proper async setup with auth
            # Left as example for async testing pattern
            pass
