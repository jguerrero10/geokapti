from fastapi import FastAPI

from app.routes import distance, location

app = FastAPI(
    title="GeoKapti",
    description="GeoKapti is a FastAPI application that allows for location registration and management, "
    "as well as calculating distances between them. This app includes an API to create and register "
    "locations in MongoDB, measure route distances, and perform asynchronous tasks.",
    version="0.2.0",
)


app.include_router(location.router, prefix="/location")
app.include_router(distance.router, prefix="/distance")
