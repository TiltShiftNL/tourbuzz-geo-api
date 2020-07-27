from . import environmental_zone, parking, max_height, stops
from fastapi import FastAPI
from .settings import settings
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/messages")
def get_messages():
    return


@app.get("/api/v1/messages/{id}")
def get_message(id):
    return


@app.get("/api/v1/messages/{year}/{month}/{day}")
def get_messages(year, month, day):
    return


@app.post("/api/v1/messages")
def post_message():
    return


@app.delete("/api/v1/messages")
def delete_message():
    return


@app.get("/api/v1/stops")
def get_stops_v1():
    return stops.legacy()


@app.get("/api/v1/parking")
def get_parking_v1():
    return parking.legacy()


@app.get("/api/v1/max_doorrijhoogte.json")
def get_max_height_v1():
    return max_height.legacy()


@app.get("/api/v1/milieuzones.json")
def get_environmental_zones_v1():
    return environmental_zone.legacy()


@app.get("/api/v2/max_height.geojson")
def get_max_height_v2(bounds = None):
    if bounds is None:
        return max_height.geojson_all()
    else:
        return max_height.geojson_bbox(bounds)


@app.get("/api/v2/environmental_zones.geojson")
def get_environmental_zones_v2(bounds = None):
    if bounds is None:
        return environmental_zone.geojson_all()
    else:
        return environmental_zone.geojson_bbox(bounds)

@app.get("/api/v2/parking.geojson")
def get_parking_v2(bounds = None):
    if bounds is None:
        return parking.geojson_all()
    else:
        return parking.geojson_bbox(bounds)

@app.get("/api/v2/stops.geojson")
def get_stops_v2(bounds = None):
    if bounds is None:
        return stops.geojson_all()
    else:
        return stops.geojson_bbox(bounds)
