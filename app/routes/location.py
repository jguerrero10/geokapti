from uuid import uuid4

from fastapi import APIRouter, Depends, status

from app.db import db as default_db
from app.logger import logger
from app.models import Location, LocationRegister

router = APIRouter()


@router.post("/", response_model=LocationRegister, status_code=status.HTTP_201_CREATED)
async def register_location(location: Location, db=Depends(lambda: default_db)):
    location_id = str(uuid4())
    location_data = dict(location)
    location_data["_id"] = location_id
    await db.locations.insert_one(location_data)
    logger.info(
        "location registered successfully",
        location_id=location_id,
        location=dict(location),
    )
    return {**location_data}
