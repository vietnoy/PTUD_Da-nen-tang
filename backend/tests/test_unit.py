"""Tests for Unit service functionality."""

from unittest.mock import Mock, patch

import pytest
from app.models import Unit
from app.schemas.Admin.UnitOfMeasurement.unitOfMeasurement import (
    CreateUnitRequest,
    CreateUnitResponse,
    DeleteUnitRequest,
    DeleteUnitResponse,
    EditUnitRequest,
    EditUnitResponse,
    GetAllUnitsRequest,
    GetAllUnitsResponse,
)
from app.services.unit import UnitService
from app.utils.responseCodeEnums import ResponseCode
from fastapi import HTTPException
from sqlalchemy.orm import Session


class TestUnitService:
    """Test cases for UnitService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock(spec=Session)

    @pytest.fixture
    def sample_unit(self):
        """Create a sample unit for testing."""
        unit = Mock(spec=Unit)
        unit.id = 1
        unit.unit_name = "kilogram"
        unit.created_at = "2023-01-01T00:00:00Z"
        unit.updated_at = "2023-01-01T00:00:00Z"
        return unit

    def test_create_unit_success(self, mock_db, sample_unit):
        """Test successful unit creation."""
        # Arrange
        request = CreateUnitRequest(unitName="kilogram")
        mock_db.query().filter().first.return_value = None  # No existing unit
        mock_db.add = Mock()
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Mock the new unit creation
        new_unit = sample_unit
        with patch("app.services.unit.Unit", return_value=new_unit):
            # Act
            result = UnitService.create_unit(mock_db, request)

            # Assert
            assert isinstance(result, CreateUnitResponse)
            assert result.unit.unit_name == "kilogram"
            assert result.result_code == ResponseCode.CREATE_UNIT_SUCCESS.value[0]
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()

    def test_create_unit_already_exists(self, mock_db, sample_unit):
        """Test unit creation when unit already exists."""
        # Arrange
        request = CreateUnitRequest(unitName="kilogram")
        mock_db.query().filter().first.return_value = sample_unit  # Existing unit

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            UnitService.create_unit(mock_db, request)

        assert exc_info.value.status_code == 400
        assert ResponseCode.UNIT_NAME_EXISTS.value[1] in str(exc_info.value.detail)

    def test_delete_unit_success(self, mock_db, sample_unit):
        """Test successful unit deletion."""
        # Arrange
        request = DeleteUnitRequest(unitName="kilogram")
        mock_db.query().filter().first.return_value = sample_unit
        mock_db.delete = Mock()
        mock_db.commit = Mock()

        # Act
        result = UnitService.delete_unit(mock_db, request)

        # Assert
        assert isinstance(result, DeleteUnitResponse)
        assert result.result_code == ResponseCode.DELETE_UNIT_SUCCESS.value[0]
        mock_db.delete.assert_called_once_with(sample_unit)
        mock_db.commit.assert_called_once()

    def test_delete_unit_not_found(self, mock_db):
        """Test unit deletion when unit doesn't exist."""
        # Arrange
        request = DeleteUnitRequest(unitName="nonexistent")
        mock_db.query().filter().first.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            UnitService.delete_unit(mock_db, request)

        assert exc_info.value.status_code == 404
        assert ResponseCode.UNIT_NOT_FOUND_119.value[1] in str(exc_info.value.detail)

    def test_edit_unit_success(self, mock_db, sample_unit):
        """Test successful unit editing."""
        # Arrange
        request = EditUnitRequest(oldName="kilogram", newName="kg")
        mock_db.query().filter().first.return_value = sample_unit
        mock_db.commit = Mock()
        mock_db.refresh = Mock()

        # Act
        result = UnitService.edit_unit(mock_db, request)

        # Assert
        assert isinstance(result, EditUnitResponse)
        assert result.result_code == ResponseCode.UPDATE_UNIT_SUCCESS.value[0]
        assert sample_unit.unit_name == "kg"
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(sample_unit)

    def test_edit_unit_not_found(self, mock_db):
        """Test unit editing when unit doesn't exist."""
        # Arrange
        request = EditUnitRequest(oldName="nonexistent", newName="kg")
        mock_db.query().filter().first.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            UnitService.edit_unit(mock_db, request)

        assert exc_info.value.status_code == 404
        assert ResponseCode.UNIT_NOT_FOUND_119.value[1] in str(exc_info.value.detail)

    def test_get_all_units_success(self, mock_db):
        """Test successful retrieval of all units."""
        # Arrange
        request = GetAllUnitsRequest()
        units = [
            Mock(
                id=1,
                unit_name="kilogram",
                created_at="2023-01-01T00:00:00Z",
                updated_at="2023-01-01T00:00:00Z",
            ),
            Mock(
                id=2,
                unit_name="gram",
                created_at="2023-01-02T00:00:00Z",
                updated_at="2023-01-02T00:00:00Z",
            ),
        ]
        mock_query = Mock()
        mock_query.all.return_value = units
        mock_db.query.return_value = mock_query

        # Act
        result = UnitService.get_all_units(mock_db, request)

        # Assert
        assert isinstance(result, GetAllUnitsResponse)
        assert len(result.units) == 2
        assert result.units[0].unit_name == "kilogram"
        assert result.units[1].unit_name == "gram"
        assert result.result_code == ResponseCode.GET_UNITS_SUCCESS.value[0]

    def test_get_all_units_with_filter(self, mock_db):
        """Test retrieval of units with name filter."""
        # Arrange
        request = GetAllUnitsRequest(unitName="kilo")
        units = [
            Mock(
                id=1,
                unit_name="kilogram",
                created_at="2023-01-01T00:00:00Z",
                updated_at="2023-01-01T00:00:00Z",
            ),
        ]
        mock_query = Mock()
        mock_query.filter().all.return_value = units
        mock_db.query.return_value = mock_query

        # Act
        result = UnitService.get_all_units(mock_db, request)

        # Assert
        assert isinstance(result, GetAllUnitsResponse)
        assert len(result.units) == 1
        assert result.units[0].unit_name == "kilogram"
        mock_query.filter.assert_called_once()

    def test_get_all_units_empty_result(self, mock_db):
        """Test retrieval when no units exist."""
        # Arrange
        request = GetAllUnitsRequest()
        mock_query = Mock()
        mock_query.all.return_value = []
        mock_db.query.return_value = mock_query

        # Act
        result = UnitService.get_all_units(mock_db, request)

        # Assert
        assert isinstance(result, GetAllUnitsResponse)
        assert len(result.units) == 0
        assert result.result_code == ResponseCode.GET_UNITS_SUCCESS.value[0]
