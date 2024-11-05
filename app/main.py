from fastapi import FastAPI

from app.routes import distance, location

app = FastAPI()


app.include_router(location.router, prefix="/location")
app.include_router(distance.router, prefix="/distance")
