from typing import List

from fastapi import APIRouter, HTTPException, status

from app.celery_app import calculate_total_distance
from app.db import db
from app.logger import logger
from app.models import TaskResponse

router = APIRouter()


@router.post("/async", description="Calculate distance between two locations asynchronously")
async def calculate_distance_async(location_ids: List[str]):
    logger.info("Calculating distance", location_ids=location_ids)
    locations = []
    for loc_id in location_ids:
        location = await db.locations.find_one({"_id": loc_id})
        if location:
            locations.append({"latitude": location["latitude"], "longitude": location["longitude"]})
    if len(locations) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least two valid locations are required to calculate the distance.",
        )

    task = calculate_total_distance.delay(locations)
    logger.info("Task dispatched", task_id=task.id, location_ids=location_ids)
    return TaskResponse(task_id=task.id, status=task.state, total_distance=task.result)


@router.get(
    "/result/{task_id}", response_model=TaskResponse, description="Get the result of the distance calculation task"
)
async def get_distance_result(task_id: str):
    task = calculate_total_distance.AsyncResult(task_id)
    return TaskResponse(task_id=task_id, status=task.state, total_distance=task.result)
