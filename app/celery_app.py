from math import sqrt

from celery import Celery

celery_app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")


@celery_app.task
def calculate_total_distance(locations):
    total_distance = 0.0
    for i in range(len(locations) - 1):
        loc1 = locations[i]
        loc2 = locations[i + 1]
        total_distance += sqrt(
            (loc1["latitude"] - loc2["latitude"]) ** 2 + (loc1["longitude"] - loc2["longitude"]) ** 2
        )
    return total_distance
