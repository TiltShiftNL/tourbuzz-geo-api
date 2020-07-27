import json
from .models import DbStop
from .database import SessionLocal, engine
from .settings import settings
from geoalchemy2 import func


def get_base_query():
    db = SessionLocal()
    return db.query(
        DbStop.id,
        DbStop.source_url,
        DbStop.source_name,
        DbStop.source_id,
        DbStop.link_url,
        DbStop.link_title,
        DbStop.name,
        DbStop.title,
        DbStop.description,
        DbStop.spots_text,
        DbStop.spots,
        DbStop.point.ST_Transform(4326).ST_AsGeoJson())


def construct_geojson(result):
    feature_collection = {
        "type": "FeatureCollection",
        "name": "stops",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }
    for entry in result:
        out = {
            "type": "Feature",
            "id": entry[0],
            "properties": {
                "title": entry[7],
                "name": entry[6],
                "description": entry[8],
                "spots_text": entry[9],
                "spots": entry[10],
                "source": {
                    "name": entry[2],
                    "url": entry[1],
                    "id": entry[3]
                }
            },
            "geometry": json.loads(entry[11])
        }
        feature_collection["features"].append(out)
    return feature_collection


def legacy():
    result_set = {
        "haltes": {}
    }
    try:
        result = get_base_query().all()
    except:
        DbStop.__table__.create(engine)
        result = get_base_query().all()

    for entry in result:
        point = json.loads(entry[11])
        out = {
            "haltenummer": entry[3],
            "straat": entry[6],
            "locatie": entry[8],
            "capaciteit": entry[10],
            "location": {
                "lat": point["coordinates"][1],
                "lng": point["coordinates"][0]
            },
            "mapsImageUrl": "https://maps.googleapis.com/maps/api/staticmap?center=" + \
                str(point["coordinates"][1]) + "," + str(point["coordinates"][0]) + \
                "&zoom=16&size=600x300&maptype=roadmap&markers=" + \
                str(point["coordinates"][1]) + "," + str(point["coordinates"][0]) + \
                "&key=" + settings.GOOGLE_MAPS_KEY,
            "mapsUrl": "https://www.google.com/maps/?q=loc:" + \
                str(point["coordinates"][1]) + "," + str(point["coordinates"][0]),
            "beschikbaar": True,
            "_origineel": {
                "title": entry[7],
                "Lokatie": entry[11],
                "Bijzonderheden": entry[8],
                "Busplaatsen": entry[9]
            }
        }
        result_set["haltes"][entry[3]] = out
    return result_set


def geojson_bbox(bounds):
    bounds_parts = bounds.split(',')
    result = get_base_query().filter(
            func.ST_Intersects(
                func.ST_MakeEnvelope(
                    bounds_parts[0],
                    bounds_parts[1],
                    bounds_parts[2],
                    bounds_parts[3],
                    4326
                ),
                DbStop.point.ST_Transform(4326),
            )
        ).all()
    return construct_geojson(result)


def geojson_all():
    
    try:
        result = get_base_query().all()
    except:
        DbStop.__table__.create(engine)
        result = get_base_query().all()
    return construct_geojson(result)

    
