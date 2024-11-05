from unittest.mock import AsyncMock, patch

import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_register_location():
    location_data = {"name": "Test Location", "latitude": 40.712776, "longitude": -74.005974}

    mock_db = AsyncMock()
    mock_db.locations.insert_one = AsyncMock(return_value={"_id": str(ObjectId())})

    with patch("app.routes.location.default_db", mock_db):
        response = client.post("/location/", json=location_data)

        assert response.status_code == 201

        mock_db.locations.insert_one.assert_called_once()

        response_data = response.json()
        assert "name" in response_data
        assert response_data["name"] == location_data["name"]
        assert response_data["latitude"] == location_data["latitude"]
        assert response_data["longitude"] == location_data["longitude"]


@pytest.mark.asyncio
async def test_register_location_invalid_data():
    invalid_location_data = {"name": "Test Location", "longitude": -74.005974}

    with patch("app.routes.location.default_db", AsyncMock()):
        response = client.post("/location/", json=invalid_location_data)

        assert response.status_code == 422
        response_data = response.json()
        assert "detail" in response_data


@pytest.mark.asyncio
async def test_register_location_logging():
    location_data = {"name": "Test Location", "latitude": 40.712776, "longitude": -74.005974}

    location_id = "2500a86b-03ad-4c7c-9e9a-625e3d1fd544"

    mock_db = AsyncMock()
    mock_db.locations.insert_one = AsyncMock(return_value={"_id": location_id})

    with patch("app.routes.location.default_db", mock_db), patch(
        "app.routes.location.uuid4", return_value=location_id
    ), patch("app.logger.logger.info") as mock_log:
        response = client.post("/location/", json=location_data)

        assert response.status_code == 201

        mock_log.assert_called_once_with(
            "location registered successfully",
            location_id=location_id,
            location=location_data,
        )
