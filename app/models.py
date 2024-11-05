from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field

from app.enums import StatusEnum

PyObjectId = Annotated[str, BeforeValidator(str)]


class LocationBase(BaseModel):
    name: str = Field(..., title="Location name", description="The name of the location")
    latitude: float = Field(..., title="Latitude", description="The latitude of the location")
    longitude: float = Field(..., title="Longitude", description="The longitude of the location")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "latitude": 10.36288,
                    "longitude": -74.119442,
                }
            ]
        }
    }


class Location(LocationBase):
    pass


class LocationRegister(LocationBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                    "name": "Foo",
                    "latitude": 10.36288,
                    "longitude": -74.119442,
                }
            ]
        }
    }


class TaskResponse(BaseModel):
    task_id: str = Field(..., title="Task ID", description="The ID of the task")
    status: StatusEnum = Field(StatusEnum.PROCESSING, title="Task Status", description="The status of the task")
    total_distance: Optional[float] = Field(
        None, title="Total Distance", description="The total distance between locations"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"task_id": "d290f1ee-6c54-4b01-90e6-d701748f0851", "status": "Processing", "total_distance": 100}
            ]
        }
    }
